import os
import pandas as pd
import json
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from joblib import dump, load
from shared import MODEL_PATHS, PROCESSED_DIR, MEDIANS_PATH, SCALER_PATH, CHURN_PATH, MODELS, OUTPUT_DIR, RESULTS_DIR, EXPECTED_COLUMNS
from data_preparation import preprocess_user_data
from sklearn.preprocessing import StandardScaler

def model_size(model_path):
    """
    Визначає розмір моделі у байтах.
    """
    if os.path.exists(model_path):
        return os.path.getsize(model_path)
    else:
        raise FileNotFoundError(f"Модель за шляхом {model_path} не знайдено.")


def save_results_to_json(model_name, classification_report, model_size):
    """
    Зберігає результати в JSON-файл.
    """
    results_path = os.path.join(RESULTS_DIR, "model_evaluation.json")
    if os.path.exists(results_path) and os.path.getsize(results_path) > 0:
        with open(results_path, "r") as f:
            try:
                results = json.load(f)
            except json.JSONDecodeError:
                print("Файл JSON пошкоджений. Створюємо новий.")
                results = {}
    else:
        results = {}

    results[model_name] = {
        "classification_report": classification_report,
        "model_size_mb": model_size,
    }

    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, "w") as f:
        json.dump(results, f, indent=4)


def train_models(data_path):
    """
    Тренує моделі на основі наданих даних.
    """
    print(f"Завантаження даних із {data_path}...")
    data = pd.read_csv(data_path)

    if "churn" not in data.columns:
        raise ValueError("Дані не містять колонки 'churn'. Перевірте вхідний файл.")

    if "id" in data.columns:
        data = data.drop(columns=["id"])

    # Обробка пропущених значень
    print("Обробка пропущених значень...")
    if not os.path.exists(MEDIANS_PATH):
        medians = data.median(numeric_only=True).to_dict()
        with open(MEDIANS_PATH, "w") as f:
            json.dump(medians, f)
        print(f"Медіани збережено у {MEDIANS_PATH}")
    else:
        with open(MEDIANS_PATH, "r") as f:
            medians = json.load(f)

    # Заповнення пропущених значень
    for column in medians:
        if column in data.columns:
            data[column] = data[column].fillna(medians[column])

    # Масштабування числових даних
    numerical_columns = [
        "subscription_age", "bill_avg", "remaining_contract",
        "download_avg", "upload_avg", "service_failure_count"
    ]
    scaler = StandardScaler()
    scaler.fit(data[numerical_columns])
    dump(scaler, SCALER_PATH)
    print(f"Scaler збережено у {SCALER_PATH}")

    # Збереження списку колонок для scaler
    scaler_feature_names_path = os.path.join(PROCESSED_DIR, "scaler_feature_names.json")
    with open(scaler_feature_names_path, "w") as f:
        json.dump(numerical_columns, f)
    print(f"Список колонок для scaler збережено у {scaler_feature_names_path}")

    # Масштабування
    data[numerical_columns] = scaler.transform(data[numerical_columns])

    X = data.drop(columns=["churn"])
    y = data["churn"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Збереження списку ознак для моделі
    feature_names = list(X.columns)
    with open(os.path.join(PROCESSED_DIR, "feature_names.json"), "w") as f:
        json.dump(feature_names, f)
    print(f"Список ознак збережено у {PROCESSED_DIR}/feature_names.json")

    for model_name, model in MODELS.items():
        try:
            print(f"Тренування моделі {model_name}...")
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            report = classification_report(y_test, y_pred, output_dict=True)
            model_path = MODEL_PATHS[model_name]
            dump(model, model_path)
            print(f"Модель {model_name} збережена за шляхом: {model_path}")

            save_results_to_json(model_name, report, model_size(model_path) / (1024 * 1024))
        except Exception as e:
            print(f"Помилка під час навчання моделі {model_name}: {e}")



def predict(data: pd.DataFrame, model_path: str) -> pd.DataFrame:
    """
    Виконує прогноз на основі даних і моделі.

    :param data: DataFrame із даними для прогнозування.
    :param model_path: Шлях до моделі.
    :return: DataFrame із прогнозами та ймовірностями.
    """
    if not model_path or not isinstance(model_path, str):
        raise ValueError("Шлях до моделі не вказаний або некоректний.")

    model = load(model_path)

    # Завантаження порядку ознак
    feature_names_path = os.path.join(PROCESSED_DIR, "feature_names.json")
    if not os.path.exists(feature_names_path):
        raise FileNotFoundError(f"Файл {feature_names_path} не знайдено. Спочатку навчіть моделі.")

    with open(feature_names_path, "r") as f:
        feature_names = json.load(f)

    # Попередня обробка даних
    processed_data = preprocess_user_data(data, MEDIANS_PATH, SCALER_PATH)

    # Сортування колонок відповідно до порядку
    processed_data = processed_data[feature_names]

    # Прогнозування
    probabilities = model.predict_proba(processed_data)
    predictions = model.predict(processed_data)

    # Додавання прогнозів і ймовірностей до DataFrame
    data['probability_of_churn'] = (probabilities[:, 1] * 100).round(2)  # Ймовірність відтоку
    data['prediction'] = predictions  # Клас (0 або 1)

    return data


def main():
    print("Розпочато навчання моделей...")
    train_models(CHURN_PATH)
    print("Тренування завершено.")


if __name__ == "__main__":
    main()
