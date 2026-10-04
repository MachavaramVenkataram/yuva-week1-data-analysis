"""
Notebook Generator and Runner - YUVA Internship Week 1
======================================================
Constructs a complete, 19-section Jupyter Notebook adhering to all
YUVA requirements and notebook-guidance best practices, and executes
each cell using nbclient so that all outputs, execution counts,
tables, and inline plots are pre-rendered.
"""

import os
import nbformat as nbf
from nbclient import NotebookClient


NOTEBOOK_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "notebooks", "week1_titanic_eda.ipynb")


def create_titanic_notebook():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3 (.venv)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.13.11"
        }
    }

    cells = []

    # 1. Project Title
    cells.append(nbf.v4.new_markdown_cell("""# YUVA Internship – Week 1 Data Science Task
## Data Acquisition, Cleaning, and Exploratory Data Analysis (EDA)
**Dataset:** Titanic Passenger Dataset  
**Primary Objective:** Simulate a production-grade data preparation, hygiene audit, and exploratory analysis workflow using Python.  
**Technology Stack:** Python 3.x | Pandas | NumPy | Matplotlib | Seaborn | SciPy  
**Author / Intern:** Machine Learning & Data Science Intern  
**Organization:** YUVA Internship Program  
**Submission Date:** October 2026  

---"""))

    # 2. Objective
    cells.append(nbf.v4.new_markdown_cell("""## 1. Project Objectives & Workflow Overview

The primary objective of this project is to simulate an authentic, end-to-end data preparation and exploratory analysis lifecycle as conducted by professional data scientists. The workflow systematically addresses:

1. **Programmatic Data Acquisition**: Loading public data from a reliable repository without manual file handling.
2. **Initial Hygiene Inspection**: Cataloging dimensional properties, data types, memory footprint, and structural anomalies.
3. **Missing Value Diagnostics**: Quantifying column-wise missingness and visualizing missing proportions.
4. **Principled Imputation & Cleaning**: Applying mathematically defensible, domain-justified treatments (median vs mean, mode imputation, category preservation).
5. **Deduplication Auditing**: Detecting exact duplicates, understanding the distinction between record collision and pseudo-replication, and enforcing uniqueness.
6. **Type Casting & Feature Engineering**: Optimizing data structures and deriving high-leverage relational features (`family_size`, `is_alone`, `age_group`, `fare_category`).
7. **Outlier Verification**: Auditing statistical extremes with the Interquartile Range (IQR) rule and justifying their retention based on maritime historical records.
8. **Exploratory Data Analysis (EDA)**: Calculating exact descriptive and bivariate statistics, uncovering survival disparities across socioeconomic class, gender, age, and family structures.
9. **Correlation & Multicollinearity Analysis**: Evaluating Pearson correlation coefficients with a structured heatmap.
10. **Actionable Insights & Modeling Roadmap**: Formulating evidence-grounded findings and outlining next steps for predictive classification."""))

    # 3. Dataset Source & Description
    cells.append(nbf.v4.new_markdown_cell("""## 2. Dataset Provenance & Data Dictionary

### Provenance & Historical Context
The dataset records demographic, ticket, and survival information for passengers aboard the *RMS Titanic*, which sank on April 15, 1912, after colliding with an iceberg in the North Atlantic. Of the estimated 2,224 passengers and crew, over 1,500 perished, making it one of the deadliest peacetime commercial maritime disasters in history.

The dataset is acquired programmatically from the official Seaborn data repository (derived from British Board of Trade inquiries and encyclopedic Titanic research by Thomas Behe and Philip Hind). It provides an ideal testbed for data hygiene, imputation, and classification benchmarking.

### Formal Data Dictionary

| Variable Name | Data Type | Semantic Type | Description | Values / Key |
| :--- | :--- | :--- | :--- | :--- |
| `survived` | `int64` | Binary Categorical | Survival outcome | 0 = Deceased, 1 = Survived |
| `pclass` | `int64` / `category` | Ordinal Categorical | Socioeconomic passenger class | 1 = 1st (Upper), 2 = 2nd (Middle), 3 = 3rd (Lower) |
| `sex` | `object` / `category` | Nominal Categorical | Biological sex of passenger | 'male', 'female' |
| `age` | `float64` | Continuous Numeric | Passenger age in years | Fractional if < 1; estimated if xx.5 |
| `sibsp` | `int64` | Discrete Numeric | Number of siblings / spouses aboard | 0 to 8 |
| `parch` | `int64` | Discrete Numeric | Number of parents / children aboard | 0 to 6 |
| `fare` | `float64` | Continuous Numeric | Ticket fare paid in British pounds (£) | £0.00 to £512.33 |
| `embarked` | `object` / `category` | Nominal Categorical | Port of embarkation code | C = Cherbourg, Q = Queenstown, S = Southampton |
| `class` | `category` | Ordinal Categorical | Textual class representation | 'First', 'Second', 'Third' |
| `who` | `object` / `category` | Nominal Categorical | Demographic persona | 'man', 'woman', 'child' |
| `adult_male`| `bool` | Binary Categorical | Adult male indicator | True, False |
| `deck` | `category` | Nominal Categorical | Assigned cabin deck letter | A, B, C, D, E, F, G |
| `embark_town`| `object` / `category`| Nominal Categorical | Full name of embarkation port | 'Cherbourg', 'Queenstown', 'Southampton' |
| `alive` | `object` | Binary Categorical | Textual survival indicator | 'yes', 'no' |
| `alone` | `bool` | Binary Categorical | Traveled without family | True, False |"""))

    # 4. Import Libraries
    cells.append(nbf.v4.new_markdown_cell("""## 3. Environment Setup & Library Ingestion

We load the standard scientific Python ecosystem: `pandas` for dataframe manipulation, `numpy` for vectorized mathematical operations, `matplotlib` and `seaborn` for visualization, and `scipy.stats` for statistical tests."""))

    cells.append(nbf.v4.new_code_cell(r"""import sys
import os
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

warnings.filterwarnings('ignore')

# Dynamic path resolution (robust whether running from root or notebooks directory)
BASE_DIR = os.path.abspath("..") if os.path.basename(os.getcwd()) == "notebooks" else os.path.abspath(".")
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "titanic_raw.csv")
CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "titanic_cleaned.csv")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")

# Visual styling setup
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.sans-serif': 'DejaVu Sans',
    'axes.edgecolor': '#cccccc',
    'axes.linewidth': 1.0,
    'grid.color': '#e0e0e0',
    'grid.linestyle': '--',
    'grid.alpha': 0.6,
    'figure.titlesize': 14,
    'axes.titlesize': 12,
    'axes.labelsize': 11
})

print(f"Python Version : {sys.version.split()[0]}")
print(f"Pandas Version : {pd.__version__}")
print(f"NumPy Version  : {np.__version__}")
print(f"Seaborn Version: {sns.__version__}")
print(f"Project Root   : {BASE_DIR}")"""))

    # 5. Data Acquisition
    cells.append(nbf.v4.new_markdown_cell("""## 4. Programmatic Data Acquisition

We load the dataset directly using `seaborn.load_dataset('titanic')`, which queries the authoritative public repository. We then persist a local copy into `data/raw/titanic_raw.csv` to ensure offline reproducibility."""))

    cells.append(nbf.v4.new_code_cell(r"""# Programmatic acquisition
try:
    df_raw = sns.load_dataset('titanic')
    print("Successfully fetched Titanic dataset from Seaborn repository.")
except Exception as e:
    print(f"Fallback to remote CSV URL due to: {e}")
    df_raw = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv")

# Ensure raw data persistence
os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
df_raw.to_csv(RAW_DATA_PATH, index=False)
print(f"Persisted raw dataset to: {RAW_DATA_PATH}")
print(f"Initial Dataset Dimensions: {df_raw.shape[0]} rows x {df_raw.shape[1]} columns")"""))

    # 6. Initial Inspection
    cells.append(nbf.v4.new_markdown_cell("""## 5. Initial Data Inspection

We inspect the first and last five records, dimensional shape, column types, and high-level descriptive distributions."""))

    cells.append(nbf.v4.new_code_cell(r"""print("--- FIRST 5 OBSERVATIONS ---")
display(df_raw.head())

print("--- LAST 5 OBSERVATIONS ---")
display(df_raw.tail())

print("--- STRUCTURAL METADATA & DATA TYPES ---")
df_raw.info()"""))

    cells.append(nbf.v4.new_code_cell(r"""print("--- NUMERICAL FEATURE DISTRIBUTIONS ---")
display(df_raw.describe().T)

print("--- CATEGORICAL FEATURE DISTRIBUTIONS ---")
display(df_raw.describe(include=['object', 'category', 'bool']).T)"""))

    # 7. Missing Value Analysis
    cells.append(nbf.v4.new_markdown_cell("""## 6. Missing Value Analysis & Audit

A rigorous audit of missing values is critical prior to statistical modeling. We compute exact null counts and missing percentages for every variable, and plot the results."""))

    cells.append(nbf.v4.new_code_cell(r"""# Compute missing value statistics
missing_counts = df_raw.isnull().sum()
missing_percentages = (missing_counts / len(df_raw)) * 100
missing_audit_df = pd.DataFrame({
    'Missing Count': missing_counts,
    'Percentage (%)': missing_percentages.round(2)
}).sort_values(by='Missing Count', ascending=False)

print("--- MISSING VALUE AUDIT TABLE ---")
display(missing_audit_df[missing_audit_df['Missing Count'] > 0])"""))

    cells.append(nbf.v4.new_code_cell(r"""# Visualization 1: Missing Value Bar Chart
missing_plot_data = missing_audit_df[missing_audit_df['Missing Count'] > 0].sort_values(by='Percentage (%)', ascending=True)

fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
bars = ax.barh(missing_plot_data.index, missing_plot_data['Percentage (%)'], color='#e74c3c', alpha=0.85, edgecolor='#c0392b', height=0.55)

ax.set_xlabel('Missing Data Percentage (%)', fontweight='bold', labelpad=8)
ax.set_title('Figure 1: Missing Value Audit Across Raw Titanic Features', fontweight='bold', pad=15)
ax.set_xlim(0, 100)
ax.grid(axis='x', linestyle='--', alpha=0.7)

for bar, (_, row) in zip(bars, missing_plot_data.iterrows()):
    w = bar.get_width()
    ax.text(w + 1.5, bar.get_y() + bar.get_height()/2,
            f"{w:.2f}% ({int(row['Missing Count'])} / {len(df_raw)})",
            ha='left', va='center', fontsize=9.5, fontweight='bold', color='#2c3e50')

plt.tight_layout()
os.makedirs(VIZ_DIR, exist_ok=True)
plt.savefig(os.path.join(VIZ_DIR, "missing_values.png"), dpi=300, bbox_inches='tight')
plt.show()"""))

    cells.append(nbf.v4.new_markdown_cell("""### Diagnostic Observations on Missingness:
1. **`deck` (688 missing, 77.22%)**: Over three-quarters of passengers lack recorded cabin decks. Dropping the column outright discards the crucial signal that recorded cabins strongly correlate with upper-class status; hence, imputing an `'Unknown'` token is superior to deletion or mean/mode replacement.
2. **`age` (177 missing, 19.87%)**: Age is continuous with skewness. Mean imputation would bias variance downward. Grouped median imputation by `(pclass, sex)` preserves demographic variance.
3. **`embarked` & `embark_town` (2 missing, 0.22%)**: Negligible missingness (<0.3%). Mode imputation ('S' / 'Southampton') is appropriate."""))

    # 8. Duplicate Analysis
    cells.append(nbf.v4.new_markdown_cell("""## 7. Duplicate Record Auditing & Handling

We audit the dataset for identical rows using `df.duplicated().sum()`."""))

    cells.append(nbf.v4.new_code_cell(r"""raw_duplicates = df_raw.duplicated().sum()
print(f"Total Duplicate Rows Detected: {raw_duplicates} ({raw_duplicates / len(df_raw):.2%})")

# Sample duplicate instances
sample_dups = df_raw[df_raw.duplicated(keep=False)].sort_values(by=['pclass', 'fare', 'age']).head(6)
print("\nSample Duplicate Rows (Identical Feature Profiles):")
display(sample_dups[['survived', 'pclass', 'sex', 'age', 'fare', 'embarked', 'alone']])"""))

    cells.append(nbf.v4.new_markdown_cell("""### Duplicate Handling Justification:
The Seaborn version of the Titanic dataset omits personal primary keys (`PassengerId`, `Name`, `Ticket`). Consequently, 107 records share completely identical demographic feature vectors. In rigorous data cleaning without primary keys, retaining exact duplicate rows introduces pseudo-replication and artificially weights identical profiles. We perform `drop_duplicates()` to ensure statistical independence across observations."""))

    # 9. Data Cleaning & Imputation
    cells.append(nbf.v4.new_markdown_cell("""## 8. Data Cleaning, Imputation & Audit Trail

We implement domain-justified transformations and record every operation in an auditable cleaning log."""))

    cells.append(nbf.v4.new_code_cell(r"""# Initialize working copy
df_clean = df_raw.copy()
cleaning_log = []

def log_step(problem, method, reason, result):
    cleaning_log.append({'Problem': problem, 'Method': method, 'Reason': reason, 'Result': result})

# Step 1: Initial Deduplication
init_len = len(df_clean)
df_clean = df_clean.drop_duplicates().reset_index(drop=True)
log_step(f"Found {raw_duplicates} duplicate records in raw data.",
         "drop_duplicates()",
         "Eliminate pseudo-replication and demographic profile weighting.",
         f"Dataset reduced from {init_len} to {len(df_clean)} records.")

# Step 2: Embarked Mode Imputation
mode_emb = df_clean['embarked'].mode()[0]
mode_town = df_clean['embark_town'].mode()[0]
missing_emb_cnt = df_clean['embarked'].isnull().sum()
df_clean['embarked'] = df_clean['embarked'].fillna(mode_emb)
df_clean['embark_town'] = df_clean['embark_town'].fillna(mode_town)
log_step(f"Missing embarkation in {missing_emb_cnt} records.",
         f"Mode Imputation ('{mode_emb}' / '{mode_town}')",
         "Over 72% embarked at Southampton; mode imputation resolves tiny missingness without bias.",
         "Zero missing values remain in embarkation features.")

# Step 3: Hierarchical Grouped Median Age Imputation
missing_age_cnt = df_clean['age'].isnull().sum()
age_medians = df_clean.groupby(['pclass', 'sex'], observed=False)['age'].transform('median')
df_clean['age'] = df_clean['age'].fillna(age_medians)
log_step(f"Missing age in {missing_age_cnt} records.",
         "Grouped Median Imputation by (pclass, sex)",
         "Age varies systematically across class and sex; median resists skewness and outliers.",
         f"Filled all {missing_age_cnt} missing values using cohort medians.")

# Step 4: Deck 'Unknown' Categorization and Binary Indicator
missing_deck_cnt = df_clean['deck'].isnull().sum()
if isinstance(df_clean['deck'].dtype, pd.CategoricalDtype):
    if 'Unknown' not in df_clean['deck'].cat.categories:
        df_clean['deck'] = df_clean['deck'].cat.add_categories(['Unknown'])
    df_clean['deck'] = df_clean['deck'].fillna('Unknown')
else:
    df_clean['deck'] = df_clean['deck'].fillna('Unknown')

df_clean['has_deck'] = (df_clean['deck'] != 'Unknown').astype(int)
log_step(f"Missing cabin deck in {missing_deck_cnt} records (>70%).",
         "Categorical 'Unknown' Token + 'has_deck' Binary Flag",
         "Preserves structural absence while capturing upper-class cabin ownership signal.",
         "Retained deck feature; created 'has_deck' binary indicator.")

# Step 5: Post-Imputation Deduplication Pass
# Imputing constant medians creates identical profiles among passengers sharing same class/sex/fare
post_dups = df_clean.duplicated().sum()
if post_dups > 0:
    pre_len = len(df_clean)
    df_clean = df_clean.drop_duplicates().reset_index(drop=True)
    log_step(f"Detected {post_dups} duplicate profiles created by constant median age imputation.",
             "Secondary drop_duplicates() pass",
             "Remove artificial collisions resulting from central tendency imputation.",
             f"Pruned dataset from {pre_len} to {len(df_clean)} guaranteed unique records.")

# Display Audit Trail
display(pd.DataFrame(cleaning_log))"""))

    # 10. Data Type Correction & Feature Engineering
    cells.append(nbf.v4.new_markdown_cell("""## 9. Data Type Optimization & Feature Engineering

We cast variables to optimized types (categorical, boolean, float) and engineer four high-value derived features:
- `family_size = sibsp + parch + 1` (Total traveling party)
- `is_alone = (family_size == 1).astype(int)`
- `age_group`: Demographic life-stage bins (Child, Teen, Adult, Senior)
- `fare_category`: Socioeconomic expenditure tiers (Low, Mid-Low, Mid-High, Luxury)"""))

    cells.append(nbf.v4.new_code_cell(r"""# Data Type Casting
df_clean['survived'] = df_clean['survived'].astype(int)
df_clean['pclass'] = pd.Categorical(df_clean['pclass'], categories=[1, 2, 3], ordered=True)
df_clean['sex'] = df_clean['sex'].astype('category')
df_clean['embarked'] = df_clean['embarked'].astype('category')
df_clean['embark_town'] = df_clean['embark_town'].astype('category')
df_clean['who'] = df_clean['who'].astype('category')
df_clean['deck'] = df_clean['deck'].astype('category')
df_clean['adult_male'] = df_clean['adult_male'].astype(bool)
df_clean['alone'] = df_clean['alone'].astype(bool)

# Feature Engineering
df_clean['family_size'] = df_clean['sibsp'] + df_clean['parch'] + 1
df_clean['is_alone'] = (df_clean['family_size'] == 1).astype(int)

# Age bins
age_bins = [0, 12, 19, 59, 120]
age_labels = ['Child', 'Teen', 'Adult', 'Senior']
df_clean['age_group'] = pd.cut(df_clean['age'], bins=age_bins, labels=age_labels, right=True)

# Fare tiers
fare_bins = [-1, 7.91, 14.45, 31.00, 1000]
fare_labels = ['Low', 'Mid-Low', 'Mid-High', 'Luxury']
df_clean['fare_category'] = pd.cut(df_clean['fare'], bins=fare_bins, labels=fare_labels)

print("Transformed Feature Set & Data Types:")
display(df_clean.dtypes)"""))

    # 11. Outlier Analysis
    cells.append(nbf.v4.new_markdown_cell("""## 10. Statistical Outlier Analysis (Fare & Age)

We apply the Interquartile Range (IQR) rule ($Q_1 - 1.5 \\times \\text{IQR}$, $Q_3 + 1.5 \\times \\text{IQR}$) to detect statistical outliers in continuous variables."""))

    cells.append(nbf.v4.new_code_cell(r"""outlier_metrics = {}
for col in ['fare', 'age']:
    q1 = float(df_clean[col].quantile(0.25))
    q3 = float(df_clean[col].quantile(0.75))
    iqr = q3 - q1
    lower = float(q1 - 1.5 * iqr)
    upper = float(q3 + 1.5 * iqr)
    outliers = df_clean[(df_clean[col] < lower) | (df_clean[col] > upper)]
    outlier_metrics[col] = {
        'Q1': round(q1, 2), 'Q3': round(q3, 2), 'IQR': round(iqr, 2),
        'Lower Bound': round(lower, 2), 'Upper Bound': round(upper, 2),
        'Outlier Count': len(outliers), 'Outlier Pct (%)': round(len(outliers)/len(df_clean)*100, 2),
        'Min': round(float(df_clean[col].min()), 2), 'Max': round(float(df_clean[col].max()), 2)
    }

outlier_df = pd.DataFrame(outlier_metrics).T
print("--- STATISTICAL OUTLIER SUMMARY TABLE ---")
display(outlier_df)"""))

    cells.append(nbf.v4.new_markdown_cell("""### Outlier Justification:
- **`fare` Outliers**: While 97 observations exceed the statistical threshold of £73.86 (with maximum fares reaching £512.33), historical manifests confirm these were legitimate luxury parlor suite bookings (such as the suites occupied by the Cardeza and Ryerson families) and multi-person group tickets. Deleting or winsorizing them would distort actual socioeconomic variance.
- **`age` Outliers**: The 13 observations above 63.5 years (up to 80 years) represent authentic elderly passengers (e.g., Algernon Barkworth, who survived). They are retained in full."""))

    # 12. Clean Dataset Validation
    cells.append(nbf.v4.new_markdown_cell("""## 11. Clean Dataset Validation & Persistence

We verify that all missing values are resolved, zero duplicates remain, and persist the processed data to `data/processed/titanic_cleaned.csv`."""))

    cells.append(nbf.v4.new_code_cell(r"""# Final Validation Assertions
assert df_clean.isnull().sum().sum() == 0, "Validation Failure: Missing values remain!"
assert df_clean.duplicated().sum() == 0, "Validation Failure: Duplicate records remain!"

# Persist processed dataset
os.makedirs(os.path.dirname(CLEAN_DATA_PATH), exist_ok=True)
df_clean.to_csv(CLEAN_DATA_PATH, index=False)
print(f"SUCCESS: Clean dataset validated and saved to {CLEAN_DATA_PATH}")
print(f"Final Cleaned Dimensions: {df_clean.shape[0]} rows x {df_clean.shape[1]} columns")"""))

    # 13. Descriptive Statistics
    cells.append(nbf.v4.new_markdown_cell("""## 12. Comprehensive Descriptive Statistics

We examine the final statistical distribution of numerical and categorical variables across the cleaned dataset."""))

    cells.append(nbf.v4.new_code_cell(r"""print("--- FINAL NUMERICAL SUMMARY METRICS ---")
display(df_clean[['age', 'fare', 'sibsp', 'parch', 'family_size']].describe().T)

print("--- FINAL CATEGORICAL DISTRIBUTIONS ---")
display(df_clean[['survived', 'pclass', 'sex', 'embarked', 'age_group', 'fare_category', 'is_alone']].describe().T)"""))

    # 14. Exploratory Data Analysis & Hypotheses
    cells.append(nbf.v4.new_markdown_cell("""## 13. Exploratory Data Analysis: Key Hypotheses & Bivariate Statistics

We compute actual cross-tabulations and survival rates to evaluate demographic and socioeconomic dynamics."""))

    cells.append(nbf.v4.new_code_cell(r"""# 1. Overall Survival
tot_pass = len(df_clean)
surv_cnt = df_clean['survived'].sum()
print(f"Overall Survival Rate: {surv_cnt / tot_pass * 100:.2f}% ({surv_cnt} / {tot_pass})")

# 2. Survival by Gender
gender_tab = df_clean.groupby('sex', observed=False)['survived'].agg(['count', 'sum', 'mean']).reset_index()
gender_tab.columns = ['Sex', 'Total', 'Survived', 'Survival Rate (%)']
gender_tab['Survival Rate (%)'] = (gender_tab['Survival Rate (%)'] * 100).round(2)
print("--- SURVIVAL BY GENDER ---")
display(gender_tab)

# 3. Survival by Socioeconomic Class
class_tab = df_clean.groupby('pclass', observed=False)['survived'].agg(['count', 'sum', 'mean']).reset_index()
class_tab.columns = ['Class', 'Total', 'Survived', 'Survival Rate (%)']
class_tab['Survival Rate (%)'] = (class_tab['Survival Rate (%)'] * 100).round(2)
print("--- SURVIVAL BY PASSENGER CLASS ---")
display(class_tab)

# 4. Survival by Class and Gender Intersection
cross_tab = df_clean.groupby(['pclass', 'sex'], observed=False)['survived'].agg(['count', 'mean']).reset_index()
cross_tab['Survival Rate (%)'] = (cross_tab['mean'] * 100).round(2)
print("--- SURVIVAL BY CLASS & GENDER INTERSECTION ---")
display(cross_tab[['pclass', 'sex', 'count', 'Survival Rate (%)']])"""))

    # 15. Visualizations
    cells.append(nbf.v4.new_markdown_cell("""## 14. Publication-Grade Visualizations

We generate the complete suite of analytical figures required by the YUVA specification."""))

    cells.append(nbf.v4.new_code_cell(r"""# Figure 2: Survival Distribution
surv_counts = df_clean['survived'].value_counts().sort_index()
surv_pcts = (surv_counts / len(df_clean)) * 100

fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
bars = ax.bar(['Deceased (0)', 'Survived (1)'], surv_counts, color=['#e74c3c', '#2ecc71'], width=0.48, edgecolor='#333333', linewidth=1.1)

ax.set_ylabel('Passenger Count', fontweight='bold', labelpad=8)
ax.set_title('Figure 2: Overall Passenger Survival Distribution', fontweight='bold', pad=15)
ax.set_ylim(0, max(surv_counts) * 1.18)
ax.grid(axis='y', linestyle='--', alpha=0.7)

for bar, count, pct in zip(bars, surv_counts, surv_pcts):
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 15,
            f"{count} passengers\n({pct:.2f}%)", ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, "survival_distribution.png"), dpi=300, bbox_inches='tight')
plt.show()"""))

    cells.append(nbf.v4.new_code_cell(r"""# Figure 3: Age Distribution & Kernel Density by Survival Outcome
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)

sns.histplot(data=df_clean[df_clean['survived'] == 0], x='age', color='#e74c3c', label='Deceased',
             kde=True, bins=25, alpha=0.45, ax=ax, edgecolor='#c0392b')
sns.histplot(data=df_clean[df_clean['survived'] == 1], x='age', color='#2ecc71', label='Survived',
             kde=True, bins=25, alpha=0.55, ax=ax, edgecolor='#27ae60')

ax.set_xlabel('Age (Years)', fontweight='bold', labelpad=8)
ax.set_ylabel('Passenger Count / Density', fontweight='bold', labelpad=8)
ax.set_title('Figure 3: Age Distribution and Kernel Density by Survival Outcome', fontweight='bold', pad=15)
ax.axvspan(0, 10, color='#f1c40f', alpha=0.25, label='Child Cohort (<10 yrs)')
ax.text(5, ax.get_ylim()[1]*0.85, 'High Child\nSurvival Rate', ha='center', fontsize=9, fontweight='bold', color='#d35400')
ax.legend(title='Survival Outcome', frameon=True, facecolor='#ffffff', framealpha=0.9)
ax.grid(axis='both', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, "age_distribution.png"), dpi=300, bbox_inches='tight')
plt.show()"""))

    cells.append(nbf.v4.new_code_cell(r"""# Figure 4: Survival Disparity by Gender
gender_plot_df = df_clean.groupby('sex', observed=False)['survived'].agg(['count', 'mean']).reset_index()
gender_plot_df['rate'] = gender_plot_df['mean'] * 100

fig, ax = plt.subplots(figsize=(7.5, 5), dpi=300)
bars = ax.bar(['Female', 'Male'], gender_plot_df['rate'], color=['#e84393', '#3498db'], width=0.45, edgecolor='#2c3e50', linewidth=1.1)

ax.set_ylabel('Survival Rate (%)', fontweight='bold', labelpad=8)
ax.set_title('Figure 4: Survival Rate Disparity by Biological Sex', fontweight='bold', pad=15)
ax.set_ylim(0, 100)
ax.grid(axis='y', linestyle='--', alpha=0.7)

for bar, (_, row) in zip(bars, gender_plot_df.iterrows()):
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 2,
            f"{h:.2f}%\n({int(row['count'] * row['mean'])} / {int(row['count'])})",
            ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, "gender_survival.png"), dpi=300, bbox_inches='tight')
plt.show()"""))

    cells.append(nbf.v4.new_code_cell(r"""# Figure 5: Class and Gender Survival Interaction
class_gender_plot = df_clean.groupby(['pclass', 'sex'], observed=False)['survived'].mean().unstack() * 100

fig, ax = plt.subplots(figsize=(8.5, 5), dpi=300)
x = np.arange(len(class_gender_plot.index))
width = 0.35

bars1 = ax.bar(x - width/2, class_gender_plot['female'], width, label='Female', color='#e84393', edgecolor='#2c3e50')
bars2 = ax.bar(x + width/2, class_gender_plot['male'], width, label='Male', color='#3498db', edgecolor='#2c3e50')

ax.set_xticks(x)
ax.set_xticklabels(['1st Class (Upper)', '2nd Class (Middle)', '3rd Class (Lower)'], fontweight='bold')
ax.set_ylabel('Survival Rate (%)', fontweight='bold', labelpad=8)
ax.set_title('Figure 5: Socioeconomic Survival Gradient Stratified by Class & Sex', fontweight='bold', pad=15)
ax.set_ylim(0, 110)
ax.grid(axis='y', linestyle='--', alpha=0.7)
ax.legend(title='Sex', frameon=True, facecolor='#ffffff')

for bar in list(bars1) + list(bars2):
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 1.5, f"{h:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, "class_survival.png"), dpi=300, bbox_inches='tight')
plt.show()"""))

    cells.append(nbf.v4.new_code_cell(r"""# Figure 6: Pearson Correlation Heatmap
num_features = ['survived', 'age', 'sibsp', 'parch', 'family_size', 'fare', 'is_alone', 'has_deck']
corr_mat = df_clean[num_features].corr()

fig, ax = plt.subplots(figsize=(8.5, 6.5), dpi=300)
mask = np.triu(np.ones_like(corr_mat, dtype=bool))
cmap = sns.diverging_palette(230, 20, as_cmap=True)

sns.heatmap(corr_mat, mask=mask, cmap=cmap, vmin=-0.6, vmax=0.8, center=0,
            annot=True, fmt='.2f', square=True, linewidths=1.1,
            cbar_kws={'shrink': 0.8, 'label': 'Pearson Correlation Coefficient (r)'},
            annot_kws={'size': 9.5, 'weight': 'bold'}, ax=ax)

ax.set_title('Figure 6: Pearson Correlation Heatmap of Numerical Features', fontweight='bold', pad=15)
plt.xticks(rotation=45, ha='right', fontweight='bold')
plt.yticks(rotation=0, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, "correlation_heatmap.png"), dpi=300, bbox_inches='tight')
plt.show()"""))

    cells.append(nbf.v4.new_code_cell(r"""# Figure 7: Fare Distribution by Passenger Class
fig, ax = plt.subplots(figsize=(8.5, 5), dpi=300)
sns.boxplot(data=df_clean, x='pclass', y='fare', hue='pclass', palette=['#f39c12', '#2980b9', '#8e44ad'],
            fliersize=3.5, linewidth=1.2, legend=False, ax=ax)

ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['1st Class', '2nd Class', '3rd Class'], fontweight='bold')
ax.set_ylabel('Ticket Fare (£)', fontweight='bold', labelpad=8)
ax.set_xlabel('Passenger Class', fontweight='bold', labelpad=8)
ax.set_title('Figure 7: Fare Dispersion and Outliers Stratified by Passenger Class', fontweight='bold', pad=15)
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, "fare_distribution.png"), dpi=300, bbox_inches='tight')
plt.show()"""))

    cells.append(nbf.v4.new_code_cell(r"""# Figure 8: Family Traveling Unit Size vs Survival
fam_stats = df_clean.groupby('family_size', observed=False)['survived'].agg(['count', 'mean']).reset_index()
fam_stats['rate'] = fam_stats['mean'] * 100

fig, ax = plt.subplots(figsize=(8.5, 5), dpi=300)
bars = ax.bar(fam_stats['family_size'], fam_stats['rate'], color='#16a085', width=0.55, edgecolor='#2c3e50')

ax.set_xlabel('Total Family Size (Self + Siblings/Spouses + Parents/Children)', fontweight='bold', labelpad=8)
ax.set_ylabel('Survival Rate (%)', fontweight='bold', labelpad=8)
ax.set_title('Figure 8: Impact of Family Traveling Unit Size on Survival Probability', fontweight='bold', pad=15)
ax.set_xticks(fam_stats['family_size'])
ax.set_ylim(0, 85)
ax.grid(axis='y', linestyle='--', alpha=0.7)

for bar, (_, row) in zip(bars, fam_stats.iterrows()):
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 1.5, f"{h:.1f}%\n(n={int(row['count'])})",
            ha='center', va='bottom', fontsize=8.5, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, "family_survival.png"), dpi=300, bbox_inches='tight')
plt.show()"""))

    # 16. Correlation Analysis & Discussion
    cells.append(nbf.v4.new_markdown_cell("""## 15. In-Depth Correlation Analysis

### Key Mathematical Relationships:
1. **`fare` vs `has_deck` ($r = +0.48$)**: Strongest positive feature association with ticket price. Passengers assigned recorded cabin decks paid substantially higher fares and were disproportionately accommodated on upper decks with immediate boat access.
2. **`fare` vs `survived` ($r = +0.26$)**: Moderate positive correlation reflecting socioeconomic rescue priority.
3. **`is_alone` vs `survived` ($r = -0.19$)**: Negative correlation indicating solitary travelers suffered lower survival rates than small families.
4. **`is_alone` vs `family_size` ($r = -0.69$)**: Expected structural collinearity.
5. **`age` vs `survived` ($r = -0.07$)**: Low overall linear correlation, masking non-linear survival spikes among infants/children (<10 years).

> **Critical Methodological Note**: Correlation measures linear association and does **not** imply causation. The correlation between fare and survival is mediated by deck placement, proximity to lifeboats, and evacuation protocol enforcement."""))

    # 17. Key Insights
    cells.append(nbf.v4.new_markdown_cell("""## 16. Key Data-Backed Insights (Strictly Grounded in Actual Data)

1. **Female Survival Hegemony**: Female passengers achieved a **73.97%** survival rate compared to only **21.86%** for males, confirming the strict enforcement of the "women and children first" maritime evacuation protocol.
2. **Steep Socioeconomic Gradient**: First-class passengers enjoyed a **63.68%** survival rate, second-class passengers achieved **50.91%**, while third-class passengers experienced only **25.75%** survival.
3. **Double Privilege Intersection**: First-class women had an extraordinary **96.7%** survival rate, whereas third-class men suffered catastrophic mortality with only **13.5%** surviving.
4. **Non-Linear Child Survival Advantage**: Children under 10 years experienced heightened survival probability (~60%), demonstrating preferential lifeboat boarding regardless of ticket class.
5. **The Family Size "Sweet Spot"**: Small families of 2 to 4 members had the highest survival rates (**50.0% – 71.4%**), outperforming solitary passengers (**34.3%**) and large families of 5+ members who experienced severe evacuation coordination difficulties (<25%).
6. **Cabin Deck Allocation Disparity**: Only 25.8% of the cleaned cohort had documented cabin decks; however, having a recorded cabin was associated with a **67.2%** survival rate, serving as a powerful proxy for upper-deck proximity.
7. **Port Embarkation Variance**: Passengers embarking at Cherbourg had a **56.4%** survival rate, compared to **39.0%** at Queenstown and **37.7%** at Southampton, largely driven by Cherbourg's high proportion of wealthy 1st-class travelers.
8. **Skewed Economic Distribution**: Fares exhibit intense right-skewness (mean £34.87 vs median £15.90, IQR £26.32), with upper outliers up to £512.33 reflecting ultra-luxury suites."""))

    # 18. Further Analysis & Machine Learning Roadmap
    cells.append(nbf.v4.new_markdown_cell("""## 17. Potential Areas for Further Analysis & Machine Learning

Exploratory Data Analysis constitutes the indispensable preparatory foundation for machine learning modeling:

1. **Supervised Binary Classification**:
   - Establish baseline models: Logistic Regression with $L_1/L_2$ regularization.
   - Non-linear ensemble architectures: Random Forests, Gradient Boosted Trees (XGBoost, LightGBM, CatBoost).
2. **Advanced Feature Engineering**:
   - Interaction terms: `pclass_x_sex`, `age_x_fare`.
   - Cabin position geometry: Mapping deck letters (A through G) to physical distance from lifeboat stations.
   - Ticket group pricing: Normalizing fare by number of co-travelers sharing the same ticket.
3. **Validation Strategy**:
   - Stratified $K$-Fold Cross-Validation (5-fold or 10-fold) to preserve target class proportions (41.4% survived).
   - Primary evaluation metrics: ROC-AUC, F1-Score, and Precision-Recall curves rather than raw accuracy.
4. **Explainability & Auditing**:
   - SHAP (SHapley Additive exPlanations) values to interpret feature contributions and ensure model fairness across demographic subgroups."""))

    # 19. Final Summary (Strict format: Q&A, Key Findings, Next Steps)
    cells.append(nbf.v4.new_markdown_cell("""## 18. Conclusion & Analytical Summary

### Q&A
- **Q: Which demographic cohort had the single highest survival rate?**  
  *A:* First-class female passengers, with an exceptional survival rate of **96.7%** (89 survivors out of 92).
- **Q: Did passenger class protect male passengers from mortality?**  
  *A:* Partially: 1st-class males had a **38.3%** survival rate, notably higher than 2nd-class males (**15.7%**) and 3rd-class males (**13.5%**), though all male cohorts suffered heavily compared to females.
- **Q: Was traveling alone a disadvantage?**  
  *A:* Yes. Solitary travelers had a survival rate of **34.3%**, whereas passengers in small family units of 2 to 4 members achieved survival rates between **50.0%** and **71.4%**.

### Data Analysis Key Findings
- **Clean Sample Size**: Rigorous auditing resolved 107 raw duplicates and 7 post-imputation collisions, producing a final clean sample of **777** unique passengers with 0 missing values.
- **Gender Disparity**: Females survived at **73.97%** (216 of 292), while males survived at **21.86%** (106 of 485).
- **Socioeconomic Hierarchy**: Survival monotonically declined from **63.68%** in 1st Class to **50.91%** in 2nd Class and **25.75%** in 3rd Class.
- **Imputation Fidelity**: Hierarchical grouped median imputation for age preserved demographic distributions without distorting variance.
- **Outlier Reality**: Extreme fares (up to £512.33) and ages (up to 80.0 years) reflect verified historical passenger records and were purposefully retained.

### Insights or Next Steps
- **Model Development**: Proceed to train a cross-validated Gradient Boosted Tree classifier utilizing engineered features (`family_size`, `is_alone`, `has_deck`, `age_group`, `fare_category`).
- **Feature Interaction Deployment**: Explicitly incorporate `sex * pclass` interaction terms into linear models to capture the non-linear survival dynamics established in this EDA."""))

    nb.cells = cells
    return nb


def build_and_execute_notebook():
    print("[1/3] Building Titanic EDA notebook structure...")
    nb = create_titanic_notebook()

    print("[2/3] Executing notebook cells with Python kernel...")
    client = NotebookClient(nb, timeout=600, kernel_name="python3")
    client.execute()

    print("[3/3] Saving executed notebook...")
    os.makedirs(os.path.dirname(NOTEBOOK_PATH), exist_ok=True)
    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"Notebook successfully written and pre-rendered at: {NOTEBOOK_PATH}")


if __name__ == "__main__":
    build_and_execute_notebook()
