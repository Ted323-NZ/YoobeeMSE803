from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MPL_CONFIG_DIR = OUTPUT_DIR / ".matplotlib"
MPL_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CONFIG_DIR))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


DATA_PATH = BASE_DIR / "data" / "Iris.csv"


def load_and_clean_data() -> tuple[pd.DataFrame, dict[str, int]]:
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()

    cleaning_summary = {
        "original_rows": len(df),
        "missing_values_before": int(df.isna().sum().sum()),
    }

    if "Id" in df.columns:
        df = df.drop(columns=["Id"])

    cleaning_summary["duplicate_rows_after_id_removed"] = int(df.duplicated().sum())

    df = df.dropna()
    df = df.drop_duplicates()
    df["Species"] = df["Species"].str.replace("Iris-", "", regex=False)

    cleaning_summary["rows_after_cleaning"] = len(df)
    cleaning_summary["missing_values_after"] = int(df.isna().sum().sum())

    return df, cleaning_summary


def save_visualisations(df: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid")

    pairplot = sns.pairplot(df, hue="Species", diag_kind="hist")
    pairplot.fig.suptitle("Iris Dataset Feature Relationships", y=1.02)
    pairplot.savefig(OUTPUT_DIR / "iris_pairplot.png", dpi=180, bbox_inches="tight")
    plt.close(pairplot.fig)


def train_and_evaluate(df: pd.DataFrame) -> dict[str, object]:
    feature_columns = [
        "SepalLengthCm",
        "SepalWidthCm",
        "PetalLengthCm",
        "PetalWidthCm",
    ]

    X = df[feature_columns]
    y = df["Species"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("svm", SVC(kernel="linear")),
        ]
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    labels = sorted(y.unique())
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0,
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "labels": labels,
        "confusion_matrix": confusion_matrix(y_test, y_pred, labels=labels),
        "classification_report": classification_report(
            y_test,
            y_pred,
            labels=labels,
            target_names=labels,
            zero_division=0,
        ),
    }


def save_results(cleaning_summary: dict[str, int], results: dict[str, object]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    result_text = (
        "Week 6 Activity 1: SVM Classification - Iris Dataset\n"
        "====================================================\n\n"
        "Cleaning Summary\n"
        "----------------\n"
        f"Original rows: {cleaning_summary['original_rows']}\n"
        f"Missing values before cleaning: {cleaning_summary['missing_values_before']}\n"
        "Duplicate rows after removing Id column: "
        f"{cleaning_summary['duplicate_rows_after_id_removed']}\n"
        f"Rows after cleaning: {cleaning_summary['rows_after_cleaning']}\n"
        f"Missing values after cleaning: {cleaning_summary['missing_values_after']}\n\n"
        "Testing Dataset Evaluation Metrics\n"
        "----------------------------------\n"
        f"Accuracy: {results['accuracy']:.4f}\n"
        f"Weighted precision: {results['precision']:.4f}\n"
        f"Weighted recall: {results['recall']:.4f}\n"
        f"Weighted F1-score: {results['f1']:.4f}\n\n"
        "Classification Report\n"
        "---------------------\n"
        f"{results['classification_report']}\n"
        "Confusion Matrix\n"
        "----------------\n"
        f"{results['confusion_matrix']}\n"
    )

    (OUTPUT_DIR / "evaluation_results.txt").write_text(result_text, encoding="utf-8")
    print(result_text)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("SVM Linear Kernel Evaluation on Iris Testing Dataset", fontsize=14)

    sns.heatmap(
        results["confusion_matrix"],
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=results["labels"],
        yticklabels=results["labels"],
        ax=axes[0],
    )
    axes[0].set_title("Confusion Matrix")
    axes[0].set_xlabel("Predicted")
    axes[0].set_ylabel("Actual")

    axes[1].axis("off")
    metrics_text = (
        "Testing Dataset Metrics\n\n"
        f"Accuracy: {results['accuracy']:.4f}\n"
        f"Weighted precision: {results['precision']:.4f}\n"
        f"Weighted recall: {results['recall']:.4f}\n"
        f"Weighted F1-score: {results['f1']:.4f}\n\n"
        "Classification Report\n\n"
        f"{results['classification_report']}"
    )
    axes[1].text(
        0,
        1,
        metrics_text,
        va="top",
        ha="left",
        family="monospace",
        fontsize=10,
    )

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "svm_results.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df, cleaning_summary = load_and_clean_data()
    save_visualisations(df)
    results = train_and_evaluate(df)
    save_results(cleaning_summary, results)


if __name__ == "__main__":
    main()
