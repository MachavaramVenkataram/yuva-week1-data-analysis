"""
Data Cleaning and Preprocessing Module - YUVA Internship Week 1
===============================================================
Project: Data Acquisition, Cleaning, and Exploratory Data Analysis
Dataset: Titanic Passenger Dataset
Description: Implements a production-grade data cleaning and preprocessing
             pipeline using Pandas. Addresses missing values, duplicate records,
             data type conversions, outlier validation, and feature engineering
             with complete justifications for every operation.
"""

import os
import pandas as pd
import numpy as np


PROCESSED_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed", "titanic_cleaned.csv")
RAW_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw", "titanic_raw.csv")


class TitanicDataCleaner:
    """
    Encapsulates the end-to-end data cleaning, imputation, type casting,
    and validation pipeline for the Titanic dataset.
    """

    def __init__(self, df: pd.DataFrame):
        self.raw_df = df.copy()
        self.df = df.copy()
        self.cleaning_log = []

    def log_operation(self, problem: str, method: str, reason: str, result: str):
        """Records metadata for each transformation to support auditability."""
        self.cleaning_log.append({
            "Problem": problem,
            "Method": method,
            "Reason": reason,
            "Result": result
        })

    def handle_duplicates_initial(self, drop: bool = True) -> int:
        """
        Detects and handles intrinsic duplicate records in raw data.
        
        Rationale:
            The raw Seaborn dataset omits unique primary identifiers (PassengerId, Name, Ticket).
            As a result, 107 records possess identical feature profiles across all 15 columns.
            Removing these duplicate records prevents pseudo-replication and artificial weighting
            in subsequent statistical analyses.
        """
        dup_count = int(self.df.duplicated().sum())
        initial_count = len(self.df)
        if dup_count > 0 and drop:
            self.df = self.df.drop_duplicates().reset_index(drop=True)
            new_count = len(self.df)
            self.log_operation(
                problem=f"Found {dup_count} intrinsic duplicate rows ({dup_count/initial_count:.2%}) lacking unique primary keys.",
                method="drop_duplicates() on raw records",
                reason="Eliminate identical demographic records to avoid sample weighting bias and pseudo-replication.",
                result=f"Dataset reduced from {initial_count} to {new_count} distinct observations."
            )
        else:
            self.log_operation(
                problem="Duplicate check on raw data.",
                method="Audit only.",
                reason="Recorded duplicate count without mutation.",
                result=f"Retained all {len(self.df)} records."
            )
        return dup_count

    def handle_missing_values(self):
        """
        Applies domain-justified imputation strategies for missing values.
        
        Strategies:
            - age: Grouped median by (pclass, sex). Outlier-resistant and context-aware.
            - embarked & embark_town: Mode imputation ('S' / 'Southampton').
            - deck: Explicit 'Unknown' categorization due to 77.2% missingness.
        """
        # 1. Embarked and embark_town (2 missing values, < 0.3%)
        emb_mode = self.df["embarked"].mode()[0]
        town_mode = self.df["embark_town"].mode()[0]
        missing_emb = int(self.df["embarked"].isnull().sum())
        
        self.df["embarked"] = self.df["embarked"].fillna(emb_mode)
        self.df["embark_town"] = self.df["embark_town"].fillna(town_mode)
        
        self.log_operation(
            problem=f"Missing port of embarkation in {missing_emb} records ({missing_emb/len(self.df):.2%}).",
            method=f"Categorical Mode Imputation ('{emb_mode}' / '{town_mode}').",
            reason="Over 72% of all passengers embarked at Southampton; mode imputation resolves negligible missingness without distortion.",
            result=f"All missing values in 'embarked' and 'embark_town' resolved to '{emb_mode}'."
        )

        # 2. Age (Continuous with skew and potential outliers)
        missing_age_before = int(self.df["age"].isnull().sum())
        overall_median = self.df["age"].median()
        
        # Calculate grouped medians by pclass and sex for granular precision
        grouped_medians = self.df.groupby(["pclass", "sex"])["age"].transform("median")
        self.df["age"] = self.df["age"].fillna(grouped_medians)
        
        self.log_operation(
            problem=f"Missing age in {missing_age_before} records ({missing_age_before/len(self.df):.2%}).",
            method="Hierarchical Grouped Median Imputation by (pclass, sex).",
            reason="Age varies systematically across socioeconomic classes and genders. Median is robust to skewness and outliers compared to mean.",
            result=f"All {missing_age_before} missing age values filled using respective demographic cohort medians (Overall median: {overall_median:.1f})."
        )

        # 3. Deck (Cabin level) - Excessive missingness (>70%)
        missing_deck_before = int(self.df["deck"].isnull().sum())
        # Convert category to include 'Unknown' or treat as object string then category
        if isinstance(self.df["deck"].dtype, pd.CategoricalDtype):
            if "Unknown" not in self.df["deck"].cat.categories:
                self.df["deck"] = self.df["deck"].cat.add_categories(["Unknown"])
            self.df["deck"] = self.df["deck"].fillna("Unknown")
        else:
            self.df["deck"] = self.df["deck"].fillna("Unknown")
            
        # Also create a binary indicator feature: has_deck_assigned
        self.df["has_deck"] = (self.df["deck"] != "Unknown").astype(int)
        
        self.log_operation(
            problem=f"Missing cabin deck in {missing_deck_before} records ({missing_deck_before/len(self.df):.2%}).",
            method="Categorical 'Unknown' Token Imputation + 'has_deck' binary indicator feature.",
            reason="Dropping deck discards valuable signal (first-class passengers had documented cabins); mean/mode imputation would be fabricated. Retaining 'Unknown' captures structural absence.",
            result=f"Deck column preserved with 'Unknown' category; binary 'has_deck' indicator created."
        )

    def handle_duplicates_post_imputation(self, drop: bool = True) -> int:
        """
        Detects and handles artificial collisions created when missing age was
        replaced with constant cohort medians.
        """
        dup_post = int(self.df.duplicated().sum())
        if dup_post > 0 and drop:
            initial = len(self.df)
            self.df = self.df.drop_duplicates().reset_index(drop=True)
            self.log_operation(
                problem=f"Detected {dup_post} post-imputation duplicate records created by cohort median age assignment.",
                method="Secondary drop_duplicates() pass",
                reason="Median age imputation assigns identical age values to records sharing the same class, sex, and fare, causing demographic collisions.",
                result=f"Dataset pruned from {initial} to {len(self.df)} guaranteed unique feature profiles."
            )
        return dup_post

    def correct_data_types(self):
        """
        Casts each column to its optimal, semantically appropriate data type
        while maintaining full numeric precision to avoid artificial collisions.
        """
        self.df["survived"] = self.df["survived"].astype(int)
        self.df["pclass"] = pd.Categorical(self.df["pclass"], categories=[1, 2, 3], ordered=True)
        self.df["sex"] = self.df["sex"].astype("category")
        self.df["embarked"] = self.df["embarked"].astype("category")
        self.df["embark_town"] = self.df["embark_town"].astype("category")
        self.df["who"] = self.df["who"].astype("category")
        self.df["deck"] = self.df["deck"].astype("category")
        self.df["age"] = self.df["age"].astype(float)
        self.df["fare"] = self.df["fare"].astype(float)
        self.df["adult_male"] = self.df["adult_male"].astype(bool)
        self.df["alone"] = self.df["alone"].astype(bool)

        self.log_operation(
            problem="Inappropriate or unoptimized data types (e.g. integer pclass, unconstrained string categories).",
            method="Explicit Pandas Type Casting (Categorical, Ordered Categorical, Boolean, Float64).",
            reason="Categorical types optimize memory footprint and enforce domain constraints; ordered categories encode socioeconomic gradient.",
            result="Optimized memory usage, ensured correct categorical behavior for modeling and visualization."
        )

    def engineer_features(self):
        """
        Derives informative domain features:
        - family_size: sibsp + parch + 1 (total members traveling together)
        - is_alone: 1 if traveling alone, 0 otherwise
        - age_group: demographic age cohorts ('Child', 'Teen', 'Adult', 'Senior')
        - fare_category: fare distribution quantiles ('Low', 'Mid-Low', 'Mid-High', 'Luxury')
        """
        # Family size
        self.df["family_size"] = self.df["sibsp"] + self.df["parch"] + 1
        self.df["is_alone"] = (self.df["family_size"] == 1).astype(int)

        # Age group bins
        age_bins = [0, 12, 19, 59, 120]
        age_labels = ["Child", "Teen", "Adult", "Senior"]
        self.df["age_group"] = pd.cut(self.df["age"], bins=age_bins, labels=age_labels, right=True)

        # Fare categories based on distribution
        fare_bins = [-1, 7.91, 14.45, 31.00, 1000]
        fare_labels = ["Low", "Mid-Low", "Mid-High", "Luxury"]
        self.df["fare_category"] = pd.cut(self.df["fare"], bins=fare_bins, labels=fare_labels)

        self.log_operation(
            problem="Raw dataset lacked composite relational features (e.g. total traveling party).",
            method="Engineered 'family_size', 'is_alone', 'age_group', and 'fare_category'.",
            reason="Captures survival dynamics (e.g. solitary travelers vs family units; vulnerable age groups).",
            result="Added 4 high-value domain features enhancing exploratory depth and predictive capability."
        )

    def analyze_outliers(self) -> dict:
        """
        Performs statistical outlier analysis using the Interquartile Range (IQR) rule
        for Fare and Age, providing domain justifications for their treatment.
        """
        outlier_summary = {}
        for col in ["fare", "age"]:
            q1 = float(self.df[col].quantile(0.25))
            q3 = float(self.df[col].quantile(0.75))
            iqr = q3 - q1
            lower_bound = float(q1 - 1.5 * iqr)
            upper_bound = float(q3 + 1.5 * iqr)
            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
            outlier_summary[col] = {
                "Q1": round(q1, 2),
                "Q3": round(q3, 2),
                "IQR": round(iqr, 2),
                "Lower Bound": round(lower_bound, 2),
                "Upper Bound": round(upper_bound, 2),
                "Outlier Count": len(outliers),
                "Outlier Pct": round((len(outliers) / len(self.df)) * 100, 2),
                "Min Value": round(float(self.df[col].min()), 2),
                "Max Value": round(float(self.df[col].max()), 2),
            }

        # Domain justification log
        self.log_operation(
            problem=f"Fare contains {outlier_summary['fare']['Outlier Count']} statistical outliers above £{outlier_summary['fare']['Upper Bound']:.2f} (max £{outlier_summary['fare']['Max Value']:.2f}).",
            method="Retained legitimate historical observations without truncation or deletion.",
            reason="Extreme fares reflect genuine high-class luxury parlour suite tickets (e.g. Cardeza and Ryerson suites) and group bookings. Truncating would distort real socioeconomic variance.",
            result="Preserved 100% of authentic historical passenger records without artificial data suppression."
        )

        return outlier_summary

    def run_cleaning_pipeline(self, save_path: str = PROCESSED_DATA_PATH) -> pd.DataFrame:
        """Executes all cleaning steps in sequence, validates integrity, and saves output."""
        print("[1/6] Auditing and removing intrinsic duplicate records from raw data...")
        self.handle_duplicates_initial(drop=True)

        print("[2/6] Performing domain-justified missing value imputations...")
        self.handle_missing_values()

        print("[3/6] Auditing and resolving post-imputation demographic collisions...")
        self.handle_duplicates_post_imputation(drop=True)

        print("[4/6] Correcting and optimizing data types...")
        self.correct_data_types()

        print("[5/6] Engineering derived domain features...")
        self.engineer_features()

        print("[6/6] Conducting statistical outlier analysis...")
        self.analyze_outliers()

        # Final Validation
        null_count = int(self.df.isnull().sum().sum())
        dup_count = int(self.df.duplicated().sum())
        assert null_count == 0, f"Validation Error: {null_count} unhandled missing values remain!"
        assert dup_count == 0, f"Validation Error: {dup_count} duplicate rows remain!"

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        self.df.to_csv(save_path, index=False)
        print(f" -> Cleaned dataset successfully persisted to: {save_path}")
        print(f" -> Final Cleaned Dimensions: {self.df.shape[0]} rows x {self.df.shape[1]} columns.\n")

        return self.df

    def get_cleaning_log_df(self) -> pd.DataFrame:
        """Returns the logged transformation rationale as a clean DataFrame."""
        return pd.DataFrame(self.cleaning_log)


def clean_titanic_data(raw_data_path: str = RAW_DATA_PATH, save_path: str = PROCESSED_DATA_PATH) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """
    Convenience functional entry point for data cleaning.
    
    Returns:
        (cleaned_df, cleaning_log_df, outlier_summary)
    """
    if os.path.exists(raw_data_path):
        df_raw = pd.read_csv(raw_data_path)
    else:
        import seaborn as sns
        df_raw = sns.load_dataset("titanic")

    cleaner = TitanicDataCleaner(df_raw)
    cleaned_df = cleaner.run_cleaning_pipeline(save_path=save_path)
    log_df = cleaner.get_cleaning_log_df()
    outlier_dict = cleaner.analyze_outliers()

    return cleaned_df, log_df, outlier_dict


if __name__ == "__main__":
    cleaned_df, log_df, outliers = clean_titanic_data()
    print("="*75)
    print("                      DATA CLEANING AUDIT TRAIL")
    print("="*75)
    for idx, row in log_df.iterrows():
        print(f"Step {idx+1}:")
        print(f"  Problem: {row['Problem']}")
        print(f"  Method : {row['Method']}")
        print(f"  Reason : {row['Reason']}")
        print(f"  Result : {row['Result']}\n")
    print("Outlier Metrics:")
    for col, metrics in outliers.items():
        print(f"  {col.upper()}: {metrics}")
