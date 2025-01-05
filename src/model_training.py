import pandas as pd
import joblib
import os
from data_preparation import preprocess_user_data
from src.graph_processing import ModelEvaluationVisualizer


# Шлях до збереженої моделі
model_path = os.path.join(os.getcwd(), 'models', 'model_RandomForest.joblib')

# Отримуємо абсолютний шлях до кореневої директорії проекту
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Шляхи до файлів
scaler_path = os.path.join(BASE_DIR, "../data/processed/scaler.pkl")
results_path = os.path.join(BASE_DIR, "../results", "model_evaluation.json")

output_dir = os.path.join(BASE_DIR, "../results")

# перевірка наявності файла
os.makedirs(output_dir, exist_ok=True)

for path in [model_path, scaler_path]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл не знайдено: {path}")


# Очікувані стовпці
EXPECTED_COLUMNS = [
    "subscription_age", "bill_avg", "reamining_contract",
    "download_avg", "upload_avg", "is_tv_subscriber",
    "is_movie_package_subscriber", "download_over_limit",
    "service_failure_count"
]

def ensure_columns(data: pd.DataFrame, expected_columns: list) -> pd.DataFrame:
    """
    Гарантує, що всі очікувані стовпці присутні та розташовані в правильному порядку.
    """
    for column in expected_columns:
        if column not in data.columns:
            data[column] = None  # Додати відсутній стовпець із значенням None
    return data[expected_columns]  # Гарантуємо порядок ознак

def predict(data: pd.DataFrame) -> pd.DataFrame:
    model = joblib.load(model_path)

    # Визначення очікуваного порядку колонок
    expected_order = [
        'is_tv_subscriber', 'is_movie_package_subscriber', 'subscription_age',
        'bill_avg', 'reamining_contract', 'service_failure_count', 'download_avg',
        'upload_avg', 'download_over_limit'
    ]

    # Гарантуємо наявність і правильний порядок колонок
    data = ensure_columns(data, expected_order)
    processed_data = preprocess_user_data(data, scaler_path)

    # Перевірка порядку колонок після обробки
    processed_data = processed_data[expected_order]

    # Використання predict_proba для отримання ймовірностей
    probabilities = model.predict_proba(processed_data)

    # Чому використовується predict_proba:
    # predict_proba повертає ймовірності для кожного класу, що дозволяє оцінити,
    # наскільки модель впевнена у своєму передбаченні. Зокрема, ми використовуємо
    # ймовірність для класу "1" (відмова), щоб визначити шанс, що клієнт відмовиться.

    # Отримання ймовірностей для класу 1 (відмова) та конвертація у відсотки
    data['probability_of_churn'] = (probabilities[:, 1] * 100).round(2)

    # Додаємо колонку 'prediction'
    data['prediction'] = (probabilities[:, 1] > 0.5).astype(int)
    return data

def run_visualization():
    try:
        visualizer = ModelEvaluationVisualizer(results_path, output_dir)
        visualizer.generate_accuracy_chart()
        visualizer.generate_f1_chart()
        visualizer.generate_model_size_chart()
        print("Графіки успішно створені та збережені!")
    except Exception as e:
        print(f"Помилка під час візуалізації: {e}")

if __name__ == "__main__":
    print("Розпочато навчання моделей...")
    run_visualization()