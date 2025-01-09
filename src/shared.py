"""
Спільні змінні, шляхи, та константи
"""

import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

# Базова директорія проекту
BASE_DIR = os.getcwd()

# Шляхи до директорій
DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
RAW_DIR = os.path.join(DATA_DIR, "raw")

MODELS_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(DATA_DIR, "results")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Шляхи до файлів
TRAINING_DATA_PATH = os.path.join(PROCESSED_DIR, "training_data.csv")
NEW_DATA_PATH = os.path.join(PROCESSED_DIR, "new_data.csv")
TEST_DATA_PATH = os.path.join(PROCESSED_DIR, "test_data.csv")
EVALUATION_RESULTS_PATH = os.path.join(RESULTS_DIR, "model_evaluation.json")
MEDIANS_PATH = os.path.join(PROCESSED_DIR, "medians.json")
SCALER_PATH = os.path.join(PROCESSED_DIR, "scaler.pkl")
CHURN_PATH = os.path.join(DATA_DIR, "raw", "internet_service_churn.csv")

# Список підтримуваних моделей для донавчання
SUPPORTED_INCREMENTAL_MODELS = ["HistGradientBoosting"]

# Шляхи до моделей
MODEL_PATHS = {
    "RandomForest": os.path.join(MODELS_DIR, "model_RandomForest.joblib"),
    "GradientBoosting": os.path.join(MODELS_DIR, "model_GradientBoosting.joblib"),
    "HistGradientBoosting": os.path.join(MODELS_DIR, "model_HistGradientBoosting.joblib"),
    "LogisticRegression": os.path.join(MODELS_DIR, "model_LogisticRegression.joblib"),
    "CalibratedRandomForest": os.path.join(MODELS_DIR, "model_CalibratedRandomForest.joblib")
}

# Моделі, які підтримують донавчання
INCREMENTAL_MODEL_PATHS = {
    model: os.path.join(MODELS_DIR, f"model_{model}.joblib")
    for model in SUPPORTED_INCREMENTAL_MODELS
}

# Визначення моделей
MODELS = {
    "RandomForest": RandomForestClassifier(),
    "GradientBoosting": GradientBoostingClassifier(),
    "HistGradientBoosting": HistGradientBoostingClassifier(),
    "LogisticRegression": LogisticRegression(max_iter=800),
}

# Очікувані колонки
EXPECTED_COLUMNS = [
    "subscription_age", "bill_avg", "remaining_contract",
    "download_avg", "upload_avg", "is_tv_subscriber",
    "is_movie_package_subscriber", "download_over_limit",
    "service_failure_count", "churn"  # Додали churn
]

# Очікуваний порядок колонок для моделей
EXPECTED_ORDER = [
    "is_tv_subscriber", "is_movie_package_subscriber", "subscription_age",
    "bill_avg", "remaining_contract", "service_failure_count",
    "download_avg", "upload_avg", "download_over_limit",
]



def print_paths():
    print("Шляхи до директорій:")
    print(f"DATA_DIR: {DATA_DIR}")
    print(f"PROCESSED_DIR: {PROCESSED_DIR}")
    print(f"RAW_DIR: {RAW_DIR}")
    print(f"MODELS_DIR: {MODELS_DIR}")
    print(f"RESULTS_DIR: {RESULTS_DIR}")
    print(f"OUTPUT_DIR: {OUTPUT_DIR}")

    print("\nШляхи до файлів:")
    print(f"TRAINING_DATA_PATH: {TRAINING_DATA_PATH}")
    print(f"NEW_DATA_PATH: {NEW_DATA_PATH}")
    print(f"TEST_DATA_PATH: {TEST_DATA_PATH}")
    print(f"EVALUATION_RESULTS_PATH: {EVALUATION_RESULTS_PATH}")
    print(f"MEDIANS_PATH: {MEDIANS_PATH}")
    print(f"SCALER_PATH: {SCALER_PATH}")
    print(f"CHURN_PATH: {CHURN_PATH}")


if __name__ == "__main__":
    print_paths()
