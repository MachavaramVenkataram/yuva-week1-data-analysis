"""
Data Acquisition Module - YUVA Internship Week 1
==================================================
Project: Data Acquisition, Cleaning, and Exploratory Data Analysis
Dataset: Titanic Passenger Dataset
Description: Programmatically loads and inspects the public Titanic passenger
             dataset from Seaborn / GitHub repository, saves a local raw copy,
             and generates comprehensive metadata summaries.
"""

import os
import sys
import pandas as pd
import seaborn as sns


# Dataset URL fallback if offline or alternative download is needed
DATA_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"
RAW_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw", "titanic_raw.csv")


def load_raw_titanic_data(save_local: bool = True, local_path: str = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Acquires the Titanic dataset programmatically.
    
    Attempts to load via Seaborn's repository cache, with a fallback to direct CSV
    download from GitHub. Optionally saves the raw dataset to data/raw/titanic_raw.csv.

    Parameters:
        save_local (bool): Whether to persist raw data to disk.
        local_path (str): Destination file path for raw CSV.

    Returns:
        pd.DataFrame: Raw Titanic DataFrame containing 891 rows and 15 features.
    """
    print("[1/3] Initiating dataset acquisition...")
    df = None
    try:
        df = sns.load_dataset("titanic")
        print(" -> Successfully loaded Titanic dataset via Seaborn repository.")
    except Exception as e:
        print(f" -> Seaborn load failed ({e}), falling back to direct URL...")
        df = pd.read_csv(DATA_URL)
        print(" -> Successfully loaded Titanic dataset from remote CSV URL.")

    if save_local and df is not None:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        df.to_csv(local_path, index=False)
        print(f" -> Raw dataset saved locally to: {local_path}")

    return df


def inspect_dataset(df: pd.DataFrame) -> dict:
    """
    Performs initial data inspection and computes dimensional metrics.

    Parameters:
        df (pd.DataFrame): Input raw dataset.

    Returns:
        dict: Inspection summary metrics.
    """
    inspection_metrics = {
        "num_rows": df.shape[0],
        "num_cols": df.shape[1],
        "columns": df.columns.tolist(),
        "shape": df.shape,
        "dtypes": df.dtypes.to_dict(),
        "duplicates": int(df.duplicated().sum()),
        "missing_counts": df.isnull().sum().to_dict(),
    }
    return inspection_metrics


def get_data_dictionary() -> pd.DataFrame:
    """
    Returns the formal data dictionary defining variables in the dataset.

    Returns:
        pd.DataFrame: Table describing variable name, type, and definition.
    """
    dictionary_data = [
        {"Variable": "survived", "Type": "int64 / Categorical", "Definition": "Survival status (0 = No, 1 = Yes)", "Key / Range": "Binary: 0 or 1"},
        {"Variable": "pclass", "Type": "int64 / Categorical", "Definition": "Socioeconomic passenger class", "Key / Range": "1 = 1st (Upper), 2 = 2nd (Middle), 3 = 3rd (Lower)"},
        {"Variable": "sex", "Type": "object / Categorical", "Definition": "Biological sex of passenger", "Key / Range": "'male', 'female'"},
        {"Variable": "age", "Type": "float64 / Continuous", "Definition": "Passenger age in years", "Key / Range": "Fractional if < 1; estimated if xx.5"},
        {"Variable": "sibsp", "Type": "int64 / Discrete", "Definition": "Count of siblings / spouses aboard", "Key / Range": "0 to 8"},
        {"Variable": "parch", "Type": "int64 / Discrete", "Definition": "Count of parents / children aboard", "Key / Range": "0 to 6"},
        {"Variable": "fare", "Type": "float64 / Continuous", "Definition": "Passenger fare in British pounds (£)", "Key / Range": "0.00 to 512.33"},
        {"Variable": "embarked", "Type": "object / Categorical", "Definition": "Port of embarkation code", "Key / Range": "C = Cherbourg, Q = Queenstown, S = Southampton"},
        {"Variable": "class", "Type": "category / Categorical", "Definition": "Textual representation of passenger class", "Key / Range": "'First', 'Second', 'Third'"},
        {"Variable": "who", "Type": "object / Categorical", "Definition": "Demographic classification (man, woman, child)", "Key / Range": "'man', 'woman', 'child'"},
        {"Variable": "adult_male", "Type": "bool / Categorical", "Definition": "Binary flag indicating whether passenger was an adult male", "Key / Range": "True or False"},
        {"Variable": "deck", "Type": "category / Categorical", "Definition": "Cabin deck letter assigned to passenger", "Key / Range": "A, B, C, D, E, F, G (High missingness)"},
        {"Variable": "embark_town", "Type": "object / Categorical", "Definition": "Full name of embarkation port", "Key / Range": "'Cherbourg', 'Queenstown', 'Southampton'"},
        {"Variable": "alive", "Type": "object / Categorical", "Definition": "Textual survival indicator", "Key / Range": "'yes', 'no'"},
        {"Variable": "alone", "Type": "bool / Categorical", "Definition": "Binary flag indicating whether passenger traveled without family", "Key / Range": "True or False"},
    ]
    return pd.DataFrame(dictionary_data)


def display_inspection_report(df: pd.DataFrame) -> None:
    """
    Prints a formatted, professional inspection summary to the console.
    """
    print("\n" + "="*70)
    print("      TITANIC PASSENGER DATASET - PRELIMINARY INSPECTION REPORT")
    print("="*70)
    print(f"Total Rows (Observations) : {df.shape[0]}")
    print(f"Total Columns (Variables) : {df.shape[1]}")
    print(f"Duplicate Records         : {df.duplicated().sum()} ({df.duplicated().sum() / len(df):.2%})")
    print(f"Memory Footprint          : {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    print("\n--- FIRST 5 ROWS ---")
    print(df.head())
    
    print("\n--- LAST 5 ROWS ---")
    print(df.tail())
    
    print("\n--- DATA TYPES & NON-NULL COUNTS ---")
    print(df.dtypes)
    
    print("\n--- MISSING VALUE AUDIT ---")
    missing_counts = df.isnull().sum()
    missing_pct = (missing_counts / len(df)) * 100
    missing_table = pd.DataFrame({"Missing Count": missing_counts, "Percentage (%)": missing_pct.round(2)})
    print(missing_table[missing_table["Missing Count"] > 0])
    
    print("\n--- DESCRIPTIVE STATISTICS (NUMERICAL) ---")
    print(df.describe())
    
    print("\n--- DESCRIPTIVE STATISTICS (CATEGORICAL / OBJECT) ---")
    print(df.describe(include=["object", "category", "bool"]))
    print("="*70 + "\n")


if __name__ == "__main__":
    df = load_raw_titanic_data()
    display_inspection_report(df)
    data_dict = get_data_dictionary()
    print("Data Dictionary:")
    print(data_dict.to_string(index=False))
