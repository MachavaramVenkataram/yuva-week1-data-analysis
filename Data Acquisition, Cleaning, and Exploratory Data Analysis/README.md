# YUVA Internship – Week 1 Data Analysis
## Titanic Passenger Directory: Data Acquisition, Cleaning & Exploratory Data Analysis (EDA)

![Python Version](https://img.shields.io/badge/Python-3.13-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Complete%20%26%20Verified-brightgreen.svg)
![Course](https://img.shields.io/badge/YUVA-Week%201%20Task-orange.svg)

---

## Overview

This repository contains the complete submission package for the **YUVA Internship – Week 1 Data Science Task**: **Data Acquisition, Cleaning, and Exploratory Data Analysis (EDA)**. 

The primary objective is to simulate an authentic, production-grade data science workflow using Python. Real-world data is seldom clean; industry benchmarks indicate that data scientists spend between 70% and 80% of their operational time sourcing, auditing, cleaning, and exploring data. This project demonstrates rigorous data hygiene, mathematically defensible imputation protocols, statistical auditing, and reproducible exploratory analysis using the **Titanic Passenger Dataset**.

---

## Objectives

The project accomplishes all 20 specific requirements outlined in the YUVA syllabus:
1. **Programmatic Data Acquisition**: Load the publicly available Titanic dataset via Seaborn repository with fallback to direct remote CSV.
2. **Initial Data Inspection**: Catalog dimensional properties, data types, summary statistics, and memory usage.
3. **Missing Value Auditing**: Quantify column-wise missing counts and percentages, accompanied by a diagnostic visualization.
4. **Duplicate Record Diagnostics**: Audit identical profiles, delineate between identifier omission and pseudo-replication, and eliminate redundancy.
5. **Principled Imputation & Cleaning**: Apply defensible imputation strategies (grouped medians, category preservation) with documented rationales.
6. **Outlier Auditing**: Statistically evaluate continuous extremes using the Interquartile Range (IQR) rule and justify their retention based on historical records.
7. **Type Casting & Feature Engineering**: Cast semantic data types and derive high-leverage relational features (`family_size`, `is_alone`, `age_group`, `fare_category`).
8. **Clean Dataset Validation**: Ensure 0 unhandled missing values, 0 duplicate records, and persist the dataset to `data/processed/titanic_cleaned.csv`.
9. **Publication-Grade Visualizations**: Generate 8 high-resolution (300 DPI) charts with clear titles, labels, legends, and diagnostic captions.
10. **Exploratory Data Analysis**: Calculate exact cross-tabulations and evaluate demographic, socioeconomic, and family dynamics.
11. **Correlation Analysis**: Compute a Pearson correlation matrix and evaluate relationships without conflating correlation with causation.
12. **Empirical Key Insights**: Formulate 8 concise, data-backed findings derived strictly from actual calculations.
13. **Executive Deliverables**: Deliver an executed, pre-rendered 19-section Jupyter Notebook (`notebooks/week1_titanic_eda.ipynb`) and a publication-quality DOCX report (`report/YUVA_Week1_Data_Analysis_Report.docx`).

---

## Dataset

- **Source**: Publicly available Titanic Passenger Directory via the Seaborn data repository (derived from British Board of Trade inquiries and encyclopedic Titanic research by Thomas Behe and Philip Hind).
- **Raw Dimensions**: 891 rows × 15 columns.
- **Cleaned Dimensions**: 777 rows × 20 columns.
- **Local Persistence**: `data/raw/titanic_raw.csv` (raw snapshot) and `data/processed/titanic_cleaned.csv` (cleaned dataset).

### Data Dictionary

| Variable | Data Type | Semantic Type | Description | Domain Key / Range |
| :--- | :--- | :--- | :--- | :--- |
| `survived` | `int64` | Binary Categorical | Survival outcome | 0 = Deceased, 1 = Survived |
| `pclass` | `category` | Ordinal Categorical | Socioeconomic passenger class | 1 = 1st (Upper), 2 = 2nd (Middle), 3 = 3rd (Lower) |
| `sex` | `category` | Nominal Categorical | Biological sex of passenger | 'male', 'female' |
| `age` | `float64` | Continuous Numeric | Passenger age in years | 0.42 to 80.0 years |
| `sibsp` | `int64` | Discrete Numeric | Number of siblings / spouses aboard | 0 to 8 |
| `parch` | `int64` | Discrete Numeric | Number of parents / children aboard | 0 to 6 |
| `fare` | `float64` | Continuous Numeric | Ticket fare paid in British pounds (£) | £0.00 to £512.33 |
| `embarked` | `category` | Nominal Categorical | Port of embarkation code | C = Cherbourg, Q = Queenstown, S = Southampton |
| `class` | `category` | Ordinal Categorical | Textual class descriptor | 'First', 'Second', 'Third' |
| `who` | `category` | Nominal Categorical | Demographic persona | 'man', 'woman', 'child' |
| `adult_male` | `bool` | Binary Categorical | Adult male indicator | True, False |
| `deck` | `category` | Nominal Categorical | Assigned cabin deck letter | A, B, C, D, E, F, G, 'Unknown' |
| `embark_town`| `category` | Nominal Categorical | Full name of embarkation port | 'Cherbourg', 'Queenstown', 'Southampton' |
| `alive` | `object` | Binary Categorical | Textual survival indicator | 'yes', 'no' |
| `alone` | `bool` | Binary Categorical | Traveled without family | True, False |
| `family_size`| `int64` | Discrete (Engineered)| Total traveling party (sibsp + parch + 1) | 1 to 11 |
| `is_alone` | `int64` | Binary (Engineered) | Solitary traveler indicator | 1 = Alone, 0 = With family |
| `age_group` | `category` | Ordinal (Engineered)| Demographic life-stage cohort | 'Child', 'Teen', 'Adult', 'Senior' |
| `fare_category`| `category`| Ordinal (Engineered)| Socioeconomic fare tier | 'Low', 'Mid-Low', 'Mid-High', 'Luxury' |
| `has_deck` | `int64` | Binary (Engineered) | Documented cabin allocation flag | 1 = Recorded, 0 = Missing |

---

## Technologies

- **Python 3.13** – Core programming language.
- **Pandas 3.0.6** – High-performance DataFrame manipulation, grouped aggregations, and type casting.
- **NumPy 2.5.3** – Vectorized numeric operations, percentile calculations, and boolean masking.
- **Matplotlib 3.11.2** – Core 2D plotting engine and canvas layout configuration.
- **Seaborn 0.13.2** – High-level statistical visualization, kernel density estimation, and heatmaps.
- **SciPy 1.18.1** – Scientific computing, IQR outlier boundaries, and statistical validation.
- **Jupyter Notebook & nbclient** – Interactive computing environment with pre-rendered execution outputs.
- **python-docx 1.2.0** – Automated generation of executive Word documents with custom styling.

---

## Project Structure

```
yuva-week1-data-analysis/
│
├── data/
│   ├── raw/
│   │   └── titanic_raw.csv                # Raw snapshot downloaded programmatically
│   └── processed/
│       └── titanic_cleaned.csv            # Cleaned, validated, 0-null processed dataset
│
├── notebooks/
│   └── week1_titanic_eda.ipynb            # Fully executed 19-section Jupyter Notebook
│
├── src/
│   ├── data_loading.py                    # Programmatic acquisition & inspection module
│   ├── data_cleaning.py                   # Production data cleaning pipeline & audit trail
│   ├── eda.py                             # Exploratory analysis & visualization generator
│   ├── generate_notebook.py               # Notebook builder & automated execution script
│   └── generate_report.py                 # Executive DOCX report compiler
│
├── visualizations/
│   ├── missing_values.png                 # Figure 1: Missing values audit chart
│   ├── survival_distribution.png          # Figure 2: Overall survival distribution
│   ├── age_distribution.png               # Figure 3: Age distribution & KDE by outcome
│   ├── gender_survival.png                # Figure 4: Survival disparity by biological sex
│   ├── class_survival.png                 # Figure 5: Socioeconomic class & sex interaction
│   ├── correlation_heatmap.png            # Figure 6: Pearson correlation matrix heatmap
│   ├── fare_distribution.png              # Figure 7: Ticket fare boxplot by class
│   └── family_survival.png                # Figure 8: Family size impact on survival
│
├── report/
│   └── YUVA_Week1_Data_Analysis_Report.docx # Complete executive Word report deliverable
│
├── requirements.txt                       # Locked project dependencies
├── README.md                              # Comprehensive project documentation
└── .gitignore                             # Clean repository exclusions
```

---

## Data Cleaning

Every preprocessing transformation was logged in an auditable data pipeline:

| Problem Identified | Method Applied | Mathematical / Domain Rationale | Result |
| :--- | :--- | :--- | :--- |
| **107 Intrinsic Duplicate Records** | `drop_duplicates()` on raw records | Seaborn dataset lacks primary keys; identical profiles cause pseudo-replication and cluster weighting bias. | Pruned raw dataset from 891 to 784 distinct observations. |
| **Missing Embarkation (2 records)** | Categorical Mode Imputation (`'S'` / `'Southampton'`) | Over 72% of all passengers embarked at Southampton; mode imputation resolves negligible missingness without distortion. | Zero missing values in `embarked` and `embark_town`. |
| **Missing Age (106 records in dedup)** | Hierarchical Grouped Median Imputation by `(pclass, sex)` | Age varies systematically across class and sex. Median is robust to skewness and extreme values compared to mean. | Imputed all missing ages using cohort medians (Class 1 Female: 35.0, Class 3 Male: 25.0). |
| **Missing Deck (582 records in dedup)** | Preserved as `'Unknown'` Token + `'has_deck'` Flag | Cabin allocation was heavily concentrated in upper classes. Deleting loses signal; imputing mode/mean is fabricated. | Retained deck feature; engineered binary `'has_deck'` indicator (25.8% positive). |
| **7 Post-Imputation Collisions** | Secondary `drop_duplicates()` pass | Imputing constant cohort medians created identical profiles among records sharing identical class, sex, and fare. | Pruned dataset from 784 to 777 guaranteed unique records. |
| **Inappropriate Data Types** | Explicit Type Casting (`category`, `bool`, `float64`) | Integer `pclass` lacks ordinal semantics; string categories waste memory and hinder modeling. | Optimized memory footprint; established ordered category for `pclass` (1 < 2 < 3). |
| **Statistical Outliers in Fare & Age** | IQR Rule Auditing + Full Retention | Fares up to £512.33 represent historical luxury parlour suites; age up to 80 represents genuine elderly travelers. | Preserved 100% of authentic historical passenger records without artificial data suppression. |

---

## Exploratory Analysis

The exploratory analysis examined the primary determinants of survival across demographic and socioeconomic dimensions:
- **Overall Survival**: In the cleaned cohort of 777 passengers, 322 survived (**41.44%**) and 455 perished (**58.56%**).
- **Gender Disparity**: Females survived at **73.97%** (216 of 292), while males survived at **21.86%** (106 of 485)—a massive net advantage of 52.11 percentage points for females, confirming strict enforcement of the "women and children first" directive.
- **Socioeconomic Gradient**: Survival probability declined monotonically with class:
  - **1st Class**: 63.68% (135 / 212)
  - **2nd Class**: 50.91% (84 / 165)
  - **3rd Class**: 25.75% (103 / 400)
- **Intersection of Privilege**: 1st-class females achieved an extraordinary **96.7%** survival rate (89 / 92), while 3rd-class males suffered catastrophic mortality with only **13.5%** surviving (35 / 259).
- **Age Dynamics**: Children under 10 years enjoyed preferential rescue (~60% survival), while young adults (ages 18–35) bore the brunt of casualties.
- **Family Traveling Units**: Small family units of 2 to 4 members had the highest survival rates (**50.0% – 71.4%**), outperforming solitary passengers (**34.3%**) and large families of 5+ members (<25%).

---

## Visualizations

All 8 figures are generated at 300 DPI and stored in the `visualizations/` directory:

1. **Figure 1: Missing Values Audit** (`visualizations/missing_values.png`) – Column-wise missing percentage breakdown across raw attributes.
2. **Figure 2: Survival Distribution** (`visualizations/survival_distribution.png`) – Overall passenger survival distribution with exact counts and percentages.
3. **Figure 3: Age Distribution & KDE** (`visualizations/age_distribution.png`) – Bimodal/unimodal age distribution stratified by survival outcome highlighting child rescue.
4. **Figure 4: Survival by Gender** (`visualizations/gender_survival.png`) – Gender survival disparity displaying the 52.1 percentage point female advantage.
5. **Figure 5: Socioeconomic Class & Gender Gradient** (`visualizations/class_survival.png`) – Multi-group bar chart showing survival rates across classes stratified by sex.
6. **Figure 6: Pearson Correlation Heatmap** (`visualizations/correlation_heatmap.png`) – Lower-triangle annotated heatmap displaying linear feature relationships.
7. **Figure 7: Fare Dispersion by Class** (`visualizations/fare_distribution.png`) – Box plot of ticket fares highlighting class stratification and historical luxury outliers.
8. **Figure 8: Family Unit Size vs Survival** (`visualizations/family_survival.png`) – Bar chart demonstrating the inverted-U curve and family size "sweet spot".

---

## Key Insights

1. **Female Survival Hegemony**: Females survived at **73.97%** compared to **21.86%** for males, confirming the strict enforcement of the Birkenhead Drill ("women and children first").
2. **Steep Socioeconomic Gradient**: First-class passengers enjoyed a **63.68%** survival rate, second-class achieved **50.91%**, and third-class experienced only **25.75%**.
3. **Double Privilege Intersection**: First-class women had an extraordinary **96.7%** survival rate, whereas third-class men suffered catastrophic mortality with only **13.5%** surviving.
4. **Non-Linear Child Survival Advantage**: Children under 10 years experienced heightened survival probability (~60%), demonstrating preferential lifeboat boarding regardless of ticket class.
5. **The Family Size "Sweet Spot"**: Small families of 2 to 4 members had the highest survival rates (**50.0% – 71.4%**), outperforming solitary passengers (**34.3%**) and large families of 5+ members who experienced severe evacuation coordination difficulties (<25%).
6. **Cabin Deck Allocation Disparity**: Only 25.8% of the cleaned cohort had documented cabin decks; however, having a recorded cabin was associated with a **67.2%** survival rate, serving as a powerful proxy for upper-deck proximity.
7. **Port Embarkation Variance**: Passengers embarking at Cherbourg had a **56.4%** survival rate, compared to **39.0%** at Queenstown and **37.7%** at Southampton, largely driven by Cherbourg's high proportion of wealthy 1st-class travelers.
8. **Skewed Economic Distribution**: Fares exhibit intense right-skewness (mean £34.87 vs median £15.90, IQR £26.32), with upper outliers up to £512.33 reflecting ultra-luxury suites.

---

## How to Run

### 1. Clone & Navigate to Repository
```bash
git clone <repository_url>
cd "yuva-week1-data-analysis"
```

### 2. Set Up Virtual Environment & Dependencies
```bash
# Windows
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Pipeline Modules
```bash
# Phase 1: Data Acquisition & Inspection
python src/data_loading.py

# Phase 2: Data Cleaning & Preprocessing
python src/data_cleaning.py

# Phase 3: Exploratory Data Analysis & Visualizations
python src/eda.py

# Phase 4: Build & Execute Jupyter Notebook
python src/generate_notebook.py

# Phase 5: Generate Final Executive Word Report
python src/generate_report.py
```

### 4. Launch Jupyter Notebook
```bash
jupyter notebook notebooks/week1_titanic_eda.ipynb
```

---

## Results & Deliverables

- **Cleaned Dataset**: [`data/processed/titanic_cleaned.csv`](data/processed/titanic_cleaned.csv) (777 rows, 20 features, 0 nulls, 0 duplicates).
- **Executed Notebook**: [`notebooks/week1_titanic_eda.ipynb`](notebooks/week1_titanic_eda.ipynb) (Pre-rendered, 42 cells, all inline outputs and charts).
- **Technical Report**: [`report/YUVA_Week1_Data_Analysis_Report.docx`](report/YUVA_Week1_Data_Analysis_Report.docx) (13-chapter, 12-table, 8-figure executive internship report).
- **Visualizations**: 8 high-resolution PNG charts in [`visualizations/`](visualizations/).

---

## Future Scope

1. **Supervised Classification Modeling**: Train and benchmark baseline Logistic Regression against Random Forests, XGBoost, and LightGBM.
2. **Feature Engineering**: Incorporate explicit `sex * pclass` and `age * pclass` interaction terms, and normalize fares by shared ticket group size.
3. **Deck Geometry Mapping**: Map cabin deck letters (A through G) to physical vertical distance from lifeboat launching stations.
4. **Explainable AI (XAI)**: Compute SHAP values to explain individual prediction attributions and audit algorithmic fairness across demographic subgroups.
