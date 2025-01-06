import pandas as pd
import joblib
import json
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from data_preparation import preprocess_user_data
from faker_new_client import generate_fake_client_data, generate_and_corrupt_data
from graph_processing import ModelEvaluationVisualizer

# Отримуємо абсолютний шлях до кореневої директорії проекту
BASE_DIR = os.getcwd()

# Шляхи до збережених моделей
MODEL_PATHS = {
    "RandomForest": os.path.join(BASE_DIR, 'models', 'model_RandomForest.joblib'),
    "GradientBoosting": os.path.join(BASE_DIR, 'models', 'model_GradientBoosting.joblib'),
    "HistGradientBoosting": os.path.join(BASE_DIR, 'models', 'model_HistGradientBoosting.joblib'),
    "LogisticRegression": os.path.join(BASE_DIR, 'models', 'model_LogisticRegression.joblib')
}
# Шляхи до файлів
medians_path = os.path.join(BASE_DIR,'data/processed/', "medians.json")
scaler_path = os.path.join(BASE_DIR, 'data/processed/', "scaler.pkl")
results_path = os.path.join(BASE_DIR, "results", "model_evaluation.json")
output_dir = os.path.join(BASE_DIR, "results")

# print(medians_path,scaler_path,results_path, output_dir)

# перевірка наявності файла
os.makedirs(output_dir, exist_ok=True)

# Очікувані стовпці
EXPECTED_COLUMNS = [
    "subscription_age", "bill_avg", "remaining_contract",
    "download_avg", "upload_avg", "is_tv_subscriber",
    "is_movie_package_subscriber", "download_over_limit",
    "service_failure_count"
]

# Функція для визначення розміру моделі
def model_size(model_path):
    """Функція для визначення розміру моделі в байтах."""
    if os.path.exists(model_path):
        return os.path.getsize(model_path)
    else:
        raise FileNotFoundError(f"Модель за шляхом {model_path} не знайдено.")

# Функція для збереження даних у JSON-файл
def save_results_to_json(model_name, classification_report, model_size):
    if os.path.exists(results_path) and os.path.getsize(results_path) > 0:
        with open(results_path, "r") as f:
            try:
                results = json.load(f)
            except json.JSONDecodeError:
                print("Файл JSON пошкоджений. Створюємо новий.")
                results = {}
    else:
        results = {}

    # Додаємо нові дані
    results[model_name] = {
        "classification_report": classification_report,
        "model_size_mb": model_size,
    }

    # Зберігаємо результати у JSON
    with open(results_path, "w") as f:
        json.dump(results, f, indent=4)


    # Додаємо дані для поточної моделі
    results[model_name] = {
        "classification_report": classification_report,
        "model_size_mb": model_size,
    }

    # Переконуємося, що директорія існує
    os.makedirs(os.path.dirname(results_path), exist_ok=True)

    # Записуємо результати у JSON-файл
    with open(results_path, "w") as f:
        json.dump(results, f, indent=4)


def ensure_columns(data: pd.DataFrame, expected_columns: list) -> pd.DataFrame:
    """
    Гарантує, що всі очікувані стовпці присутні та розташовані в правильному порядку.
    """
    for column in expected_columns:
        if column not in data.columns:
            data[column] = None  # Додати відсутній стовпець із значенням None

    # Перетворення колонок на числовий тип, якщо можливо
    for column in ["remaining_contract", "subscription_age", "bill_avg", "download_avg", "upload_avg",
                   "service_failure_count"]:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors='coerce')  # Примусове перетворення

    return data[expected_columns]  # Гарантуємо порядок ознак

def predict(data: pd.DataFrame, model_path: str) -> pd.DataFrame:
    """
    Функція для передбачення на основі даних та моделі, шлях до якої передається.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Файл моделі {model_path} не знайдено.")

    # Видалення "id", якщо він є
    if "id" in data.columns:
        data = data.drop(columns=["id"])

    # Завантажуємо модель
    model = joblib.load(model_path)

    # Визначення очікуваного порядку колонок
    expected_order = [
        'is_tv_subscriber', 'is_movie_package_subscriber', 'subscription_age',
        'bill_avg', 'remaining_contract', 'service_failure_count', 'download_avg',
        'upload_avg', 'download_over_limit'
    ]

    # Гарантуємо наявність і правильний порядок колонок
    data = ensure_columns(data, expected_order)
    data = data.fillna(0)  # Заміна None/NaN на 0
    processed_data = preprocess_user_data(data, medians_path, scaler_path)

    # Перевірка порядку колонок після обробки
    processed_data = processed_data[expected_order]

    # Використання predict_proba для отримання ймовірностей
    probabilities = model.predict_proba(processed_data)

    # Отримання ймовірностей для класу 1 (відмова) та конвертація у відсотки
    data['probability_of_churn'] = (probabilities[:, 1] * 100).round(2)

    # Додаємо колонку 'prediction'
    data['prediction'] = (probabilities[:, 1] > 0.5).astype(int)

    return data


def train_models(data_path: str):
    """
    Функція для тренування моделей на основі даних.
    """
    # Завантаження даних
    data = pd.read_csv(data_path)

    # Перевірка наявності колонки churn
    if "churn" not in data.columns:
        raise ValueError("Дані не містять колонки 'churn'. Перевірте вхідний файл.")

    # Видалення стовпця "id", якщо він присутній
    if "id" in data.columns:
        data = data.drop(columns=["id"])

    # Попередня обробка даних
    data = preprocess_user_data(data, medians_path, scaler_path)

    # Розділення даних на тренувальну і тестову вибірки
    X = data.drop(columns=["churn"])
    y = data["churn"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Тренування моделей
    models = {
        "RandomForest": RandomForestClassifier(),
        "GradientBoosting": GradientBoostingClassifier(),
        "HistGradientBoosting": HistGradientBoostingClassifier(),
        "LogisticRegression": LogisticRegression(max_iter=500)  # Збільшення кількості ітерацій
    }

    for model_name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(f"Класифікаційний звіт для {model_name}:\n")
        print(classification_report(y_test, y_pred))

        # Збереження моделі
        model_path = os.path.join(BASE_DIR, "models", f"model_{model_name}.joblib")
        joblib.dump(model, model_path)
        print(f"Модель {model_name} збережена за шляхом: {model_path}")

    return X_test, y_test  # Повертаємо тестові вибірки

def model_classification_report(model, model_name, X_test, y_test):
    """
    Функція для генерації класифікаційного звіту для конкретної моделі.

    Параметри:
        model: Навчена модель, яка підтримує методи `predict` або `predict_proba`.
        model_name: str - Назва моделі (для збереження результатів у JSON).
        X_test: pd.DataFrame - Вхідні тестові дані.
        y_test: pd.Series - Очікувані цільові значення.

    Повертає:
        dict - Класифікаційний звіт у форматі словника.
    """
    # Генерація прогнозів
    y_pred = model.predict(X_test)
    # Генерація класифікаційного звіту
    report = classification_report(y_test, y_pred, output_dict=True)
    # Визначення розміру моделі
    model_size_mb = model_size(MODEL_PATHS[model_name]) / (1024 * 1024)  # Конвертуємо байти в MB
    # Збереження результатів у JSON
    save_results_to_json(model_name, report, model_size_mb)

    print(f"Звіт для {model_name} успішно збережено.")

    return report



def run_visualization():
    try:
        # Створюємо візуалізатор
        visualizer = ModelEvaluationVisualizer(base_dir=BASE_DIR)
        visualizer.create_plots()
        print("Графіки успішно створені та збережені!")
    except FileNotFoundError as e:
        print(f"Помилка під час візуалізації: {e}")
    except Exception as e:
        print(f"Невідома помилка під час візуалізації: {e}")




if __name__ == "__main__":
    print("Розпочато навчання моделей...")

    # Тренування моделей
    train_models("data/raw/internet_service_churn.csv")

    # Генерація даних для нового клієнта
    fake_client_data = generate_fake_client_data()  # Генерація фейкових даних
    user_data = pd.DataFrame([fake_client_data])  # Конвертація в DataFrame

    # Передбачення для всіх моделей
    # Передбачення для всіх моделей та збереження результатів
    if __name__ == "__main__":
        print("Розпочато навчання моделей...")

        # Тренування моделей
        X_test, y_test = train_models("data/raw/internet_service_churn.csv")

        # Генерація даних для нового клієнта
        fake_client_data = generate_fake_client_data()  # Генерація фейкових даних
        user_data = pd.DataFrame([fake_client_data])  # Конвертація в DataFrame

        # Передбачення для всіх моделей
        for model_name, model_path in MODEL_PATHS.items():
            print(f"Генерація звіту для моделі {model_name}...")

            # Завантажуємо модель
            model = joblib.load(model_path)

            # Викликаємо універсальну функцію для класифікаційного звіту
            report = model_classification_report(model, model_name, X_test, y_test)

            print(f"Класифікаційний звіт для {model_name}:\n", report)

    # Створення візуалізацій
    run_visualization()

