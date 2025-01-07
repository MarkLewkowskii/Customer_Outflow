import pandas as pd
from joblib import load
import os
from data_preparation import preprocess_user_data
from src.graph_processing import ModelEvaluationVisualizer

# Отримуємо абсолютний шлях до кореневої директорії проекту
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)


# Шляхи до файлів
scaler_path = os.path.join(BASE_DIR, "./data/processed/scaler.pkl")
results_path = os.path.join(BASE_DIR, "./results", "model_evaluation.json")
output_dir = os.path.join(BASE_DIR, "./results")

# перевірка наявності файла
os.makedirs(output_dir, exist_ok=True)

for path in [scaler_path]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл не знайдено: {path}")

def ensure_columns(df):
    """
    Перевіряємо, що DataFrame має правильні колонки.
    """
    required_columns = [
        'is_tv_subscriber', 'is_movie_package_subscriber', 'subscription_age',
        'bill_avg', 'remaining_contract', 'service_failure_count',
        'download_avg', 'upload_avg', 'download_over_limit'
    ]
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0
    return df[required_columns]

def load_model(model_name):
    model_path = os.path.join(BASE_DIR, f"./models/model_{model_name}.joblib")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Модель {model_name} не знайдена за шляхом {model_path}")
    return load(model_path)


def predict(data: pd.DataFrame, model_name: str = "model_HistGradientBoosting.joblib") -> pd.DataFrame:
    """
    Прогнозує ймовірність відтоку для клієнтів, використовуючи вказану модель.

    :param data: DataFrame із вхідними даними.
    :param model_name: Назва моделі для завантаження.
    :return: DataFrame із прогнозами та ймовірностями.
    """
    # Завантаження моделі
    model = load_model(model_name)

    # Гарантуємо наявність правильних колонок
    data = ensure_columns(data)

    # Попередня обробка даних
    processed_data = preprocess_user_data(data, scaler_path)

    # Використання predict_proba для отримання ймовірностей
    probabilities = model.predict_proba(processed_data)

    # Додавання результатів у DataFrame
    data['probability_of_churn'] = (probabilities[:, 1] * 100).round(2)
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
