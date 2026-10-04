"""
Exploratory Data Analysis (EDA) Module - YUVA Internship Week 1
==============================================================
Project: Data Acquisition, Cleaning, and Exploratory Data Analysis
Dataset: Titanic Passenger Dataset
Description: Computes comprehensive descriptive and bivariate statistics,
             analyzes survival dynamics across demographics and socioeconomic
             tiers, and generates publication-grade visualizations saved to
             the visualizations/ directory.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


RAW_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw", "titanic_raw.csv")
PROCESSED_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed", "titanic_cleaned.csv")
VIZ_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "visualizations")


# Professional Plot Styling Configurations
plt.rcParams.update({
    "font.sans-serif": "DejaVu Sans",
    "axes.edgecolor": "#cccccc",
    "axes.linewidth": 1.0,
    "grid.color": "#e0e0e0",
    "grid.linestyle": "--",
    "grid.alpha": 0.6,
    "figure.autolayout": False,
})
PALETTE_SURVIVAL = ["#e74c3c", "#2ecc71"]  # Red = Deceased (0), Green = Survived (1)
PALETTE_GENDER = ["#3498db", "#e84393"]    # Blue = Male, Pink = Female
PALETTE_CLASS = ["#f39c12", "#2980b9", "#8e44ad"]  # 1st, 2nd, 3rd


def setup_viz_directory(dir_path: str = VIZ_DIR) -> str:
    """Ensures visualizations directory exists."""
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


def compute_summary_statistics(df: pd.DataFrame) -> dict:
    """
    Computes rigorous descriptive and bivariate statistics from the dataset.
    All numbers are dynamically derived from actual data without fabrication.
    """
    total_passengers = len(df)
    survived_count = int(df["survived"].sum())
    deceased_count = total_passengers - survived_count
    overall_survival_rate = float(df["survived"].mean() * 100)

    # Gender metrics
    gender_stats = df.groupby("sex", observed=False)["survived"].agg(["count", "sum", "mean"]).reset_index()
    gender_stats.columns = ["Sex", "Total", "Survived", "Survival_Rate"]
    gender_stats["Survival_Rate"] = (gender_stats["Survival_Rate"] * 100).round(2)

    # Class metrics
    class_stats = df.groupby("pclass", observed=False)["survived"].agg(["count", "sum", "mean"]).reset_index()
    class_stats.columns = ["Class", "Total", "Survived", "Survival_Rate"]
    class_stats["Survival_Rate"] = (class_stats["Survival_Rate"] * 100).round(2)

    # Gender & Class intersection
    gender_class_stats = df.groupby(["pclass", "sex"], observed=False)["survived"].agg(["count", "mean"]).reset_index()
    gender_class_stats["Survival_Rate"] = (gender_class_stats["mean"] * 100).round(2)

    # Age and Fare metrics
    age_mean = float(df["age"].mean())
    age_median = float(df["age"].median())
    age_std = float(df["age"].std())
    fare_mean = float(df["fare"].mean())
    fare_median = float(df["fare"].median())
    fare_std = float(df["fare"].std())

    # Family size metrics
    family_stats = df.groupby("family_size", observed=False)["survived"].agg(["count", "mean"]).reset_index()
    family_stats["Survival_Rate"] = (family_stats["mean"] * 100).round(2)

    # Embarkation metrics
    embark_stats = df.groupby("embark_town", observed=False)["survived"].agg(["count", "mean"]).reset_index()
    embark_stats.columns = ["Port", "Total", "Survival_Rate"]
    embark_stats["Survival_Rate"] = (embark_stats["Survival_Rate"] * 100).round(2)

    return {
        "total_passengers": total_passengers,
        "survived_count": survived_count,
        "deceased_count": deceased_count,
        "overall_survival_rate": round(overall_survival_rate, 2),
        "gender_stats": gender_stats,
        "class_stats": class_stats,
        "gender_class_stats": gender_class_stats,
        "age_metrics": {"mean": round(age_mean, 2), "median": round(age_median, 2), "std": round(age_std, 2)},
        "fare_metrics": {"mean": round(fare_mean, 2), "median": round(fare_median, 2), "std": round(fare_std, 2)},
        "family_stats": family_stats,
        "embark_stats": embark_stats,
    }


# =====================================================================
# VISUALIZATION GENERATORS
# =====================================================================

def plot_missing_values(raw_df: pd.DataFrame, save_path: str = None) -> str:
    """Visualization 1: Missing values count and percentage before cleaning."""
    save_path = save_path or os.path.join(VIZ_DIR, "missing_values.png")
    
    missing_counts = raw_df.isnull().sum()
    missing_pct = (missing_counts / len(raw_df)) * 100
    missing_df = pd.DataFrame({"Count": missing_counts, "Percentage": missing_pct})
    missing_df = missing_df[missing_df["Count"] > 0].sort_values(by="Percentage", ascending=True)

    fig, ax1 = plt.subplots(figsize=(10, 5), dpi=300)
    bars = ax1.barh(missing_df.index, missing_df["Percentage"], color="#e74c3c", alpha=0.85, edgecolor="#c0392b", height=0.55)

    ax1.set_xlabel("Missing Data Percentage (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax1.set_title("Figure 1: Missing Value Audit Across Raw Titanic Features", fontsize=13, fontweight="bold", pad=15)
    ax1.set_xlim(0, 100)
    ax1.grid(axis="x", linestyle="--", alpha=0.7)

    for bar, (_, row) in zip(bars, missing_df.iterrows()):
        width = bar.get_width()
        ax1.text(width + 1.5, bar.get_y() + bar.get_height()/2,
                 f"{width:.2f}% ({int(row['Count'])} / {len(raw_df)})",
                 ha="left", va="center", fontsize=9.5, fontweight="bold", color="#2c3e50")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    return save_path


def plot_survival_distribution(df: pd.DataFrame, save_path: str = None) -> str:
    """Visualization 2: Overall survival distribution (counts and proportion)."""
    save_path = save_path or os.path.join(VIZ_DIR, "survival_distribution.png")
    
    surv_counts = df["survived"].value_counts().sort_index()
    surv_pcts = (surv_counts / len(df)) * 100

    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
    labels = ["Deceased (0)", "Survived (1)"]
    bars = ax.bar(labels, surv_counts, color=PALETTE_SURVIVAL, width=0.5, edgecolor="#333333", linewidth=1.2)

    ax.set_ylabel("Passenger Count", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("Figure 2: Overall Passenger Survival Distribution", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylim(0, max(surv_counts) * 1.18)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    for bar, count, pct in zip(bars, surv_counts, surv_pcts):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 15,
                f"{count} passengers\n({pct:.2f}%)",
                ha="center", va="bottom", fontsize=10.5, fontweight="bold", color="#2c3e50")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    return save_path


def plot_age_distribution(df: pd.DataFrame, save_path: str = None) -> str:
    """Visualization 3: Age distribution stratified by survival status."""
    save_path = save_path or os.path.join(VIZ_DIR, "age_distribution.png")

    fig, ax = plt.subplots(figsize=(9.5, 5.5), dpi=300)
    
    sns.histplot(data=df[df["survived"] == 0], x="age", color="#e74c3c", label="Deceased",
                 kde=True, bins=25, alpha=0.45, ax=ax, edgecolor="#c0392b")
    sns.histplot(data=df[df["survived"] == 1], x="age", color="#2ecc71", label="Survived",
                 kde=True, bins=25, alpha=0.55, ax=ax, edgecolor="#27ae60")

    ax.set_xlabel("Age (Years)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_ylabel("Passenger Density / Count", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("Figure 3: Age Distribution and Kernel Density by Survival Outcome", fontsize=13, fontweight="bold", pad=15)
    ax.legend(title="Survival Outcome", frameon=True, facecolor="#ffffff", framealpha=0.9, fontsize=10)
    ax.grid(axis="both", linestyle="--", alpha=0.6)

    # Highlight child survival spike (< 10)
    ax.axvspan(0, 10, color="#f1c40f", alpha=0.2, label="Child Cohort (<10 yrs)")
    ax.text(5, ax.get_ylim()[1]*0.88, "High Child\nSurvival Window", ha="center", fontsize=9, fontweight="bold", color="#d35400")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    return save_path


def plot_gender_survival(df: pd.DataFrame, save_path: str = None) -> str:
    """Visualization 4: Survival rate by biological sex."""
    save_path = save_path or os.path.join(VIZ_DIR, "gender_survival.png")

    gender_df = df.groupby("sex", observed=False)["survived"].agg(["count", "mean"]).reset_index()
    gender_df["rate"] = gender_df["mean"] * 100

    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
    bars = ax.bar(["Female", "Male"], gender_df["rate"], color=["#e84393", "#3498db"], width=0.48, edgecolor="#2c3e50", linewidth=1.2)

    ax.set_ylabel("Survival Rate (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("Figure 4: Survival Disparity by Biological Sex ('Women First')", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylim(0, 100)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    for bar, (_, row) in zip(bars, gender_df.iterrows()):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 2,
                f"{h:.2f}%\n({int(row['count'] * row['mean'])} / {int(row['count'])})",
                ha="center", va="bottom", fontsize=10.5, fontweight="bold", color="#2c3e50")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    return save_path


def plot_class_survival(df: pd.DataFrame, save_path: str = None) -> str:
    """Visualization 5: Survival rate by passenger class and gender intersection."""
    save_path = save_path or os.path.join(VIZ_DIR, "class_survival.png")

    grouped = df.groupby(["pclass", "sex"], observed=False)["survived"].mean().unstack() * 100

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    x = np.arange(len(grouped.index))
    width = 0.35

    bars1 = ax.bar(x - width/2, grouped["female"], width, label="Female", color="#e84393", edgecolor="#2c3e50", linewidth=1.1)
    bars2 = ax.bar(x + width/2, grouped["male"], width, label="Male", color="#3498db", edgecolor="#2c3e50", linewidth=1.1)

    ax.set_xticks(x)
    ax.set_xticklabels(["1st Class (Upper)", "2nd Class (Middle)", "3rd Class (Lower)"], fontsize=10.5, fontweight="bold")
    ax.set_ylabel("Survival Rate (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("Figure 5: Socioeconomic Survival Gradient Stratified by Class & Gender", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylim(0, 110)
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.legend(title="Sex", frameon=True, facecolor="#ffffff", framealpha=0.9, fontsize=10)

    for bar in list(bars1) + list(bars2):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 1.5, f"{h:.1f}%",
                ha="center", va="bottom", fontsize=9.5, fontweight="bold")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    return save_path


def plot_correlation_heatmap(df: pd.DataFrame, save_path: str = None) -> str:
    """Visualization 6: Correlation matrix heatmap across numerical features."""
    save_path = save_path or os.path.join(VIZ_DIR, "correlation_heatmap.png")

    num_cols = ["survived", "age", "sibsp", "parch", "family_size", "fare", "is_alone", "has_deck"]
    corr = df[num_cols].corr()

    fig, ax = plt.subplots(figsize=(8.5, 7), dpi=300)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-0.6, vmax=0.8, center=0,
                annot=True, fmt=".2f", square=True, linewidths=1.2,
                cbar_kws={"shrink": 0.8, "label": "Pearson Correlation Coefficient (r)"},
                annot_kws={"size": 9.5, "weight": "bold"}, ax=ax)

    ax.set_title("Figure 6: Pearson Correlation Heatmap of Numerical Features", fontsize=13, fontweight="bold", pad=15)
    plt.xticks(rotation=45, ha="right", fontsize=9.5, fontweight="bold")
    plt.yticks(rotation=0, fontsize=9.5, fontweight="bold")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    return save_path


def plot_fare_distribution(df: pd.DataFrame, save_path: str = None) -> str:
    """Optional Additional Visualization 7: Box plot of fare by passenger class."""
    save_path = save_path or os.path.join(VIZ_DIR, "fare_distribution.png")

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    sns.boxplot(data=df, x="pclass", y="fare", hue="pclass", palette=PALETTE_CLASS,
                fliersize=3.5, linewidth=1.2, legend=False, ax=ax)

    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(["1st Class", "2nd Class", "3rd Class"], fontsize=10.5, fontweight="bold")
    ax.set_ylabel("Ticket Fare (£)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_xlabel("Passenger Class", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("Figure 7: Fare Dispersion and Outliers Stratified by Passenger Class", fontsize=13, fontweight="bold", pad=15)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    return save_path


def plot_family_survival(df: pd.DataFrame, save_path: str = None) -> str:
    """Optional Additional Visualization 8: Family size vs survival rate."""
    save_path = save_path or os.path.join(VIZ_DIR, "family_survival.png")

    fam_df = df.groupby("family_size", observed=False)["survived"].agg(["count", "mean"]).reset_index()
    fam_df["rate"] = fam_df["mean"] * 100

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    bars = ax.bar(fam_df["family_size"], fam_df["rate"], color="#16a085", width=0.6, edgecolor="#2c3e50")

    ax.set_xlabel("Total Family Size (Self + Siblings/Spouses + Parents/Children)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_ylabel("Survival Rate (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("Figure 8: Impact of Family Traveling Unit Size on Survival Probability", fontsize=13, fontweight="bold", pad=15)
    ax.set_xticks(fam_df["family_size"])
    ax.set_ylim(0, 85)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    for bar, (_, row) in zip(bars, fam_df.iterrows()):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 1.5, f"{h:.1f}%\n(n={int(row['count'])})",
                ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    return save_path


def generate_all_visualizations(raw_df: pd.DataFrame, clean_df: pd.DataFrame) -> dict:
    """Generates and saves all required and supplementary EDA visualizations."""
    setup_viz_directory(VIZ_DIR)
    print("Generating comprehensive visualization suite...")
    
    saved_files = {
        "missing_values": plot_missing_values(raw_df),
        "survival_distribution": plot_survival_distribution(clean_df),
        "age_distribution": plot_age_distribution(clean_df),
        "gender_survival": plot_gender_survival(clean_df),
        "class_survival": plot_class_survival(clean_df),
        "correlation_heatmap": plot_correlation_heatmap(clean_df),
        "fare_distribution": plot_fare_distribution(clean_df),
        "family_survival": plot_family_survival(clean_df),
    }

    for name, path in saved_files.items():
        print(f" -> Saved {name} to {path}")
    return saved_files


if __name__ == "__main__":
    raw_df = pd.read_csv(RAW_DATA_PATH)
    clean_df = pd.read_csv(PROCESSED_DATA_PATH)
    
    stats = compute_summary_statistics(clean_df)
    print("=== SUMMARY STATISTICS ===")
    print(f"Total Clean Passengers: {stats['total_passengers']}")
    print(f"Overall Survival Rate : {stats['overall_survival_rate']}%")
    print("\nGender Survival:\n", stats["gender_stats"])
    print("\nClass Survival:\n", stats["class_stats"])
    
    files = generate_all_visualizations(raw_df, clean_df)
    print(f"\nSuccessfully generated {len(files)} high-resolution charts in {VIZ_DIR}")
