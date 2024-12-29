import pandas as pd
import joblib
from data_preparation import preprocess_user_data
from faker_new_client import generate_fake_client_data, generate_and_corrupt_data
import os
# Шлях до збереженої моделі
model_path = os.path.join(os.getcwd(), 'models', 'model_RandomForest.joblib')


# Шляхи до медіан і scaler
import os

# Отримуємо абсолютний шлях до кореневої директорії проекту
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Шляхи до файлів
medians_path = os.path.join(BASE_DIR, "../data/processed/medians.json")
scaler_path = os.path.join(BASE_DIR, "../data/processed/scaler.pkl")

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
    processed_data = preprocess_user_data(data, medians_path, scaler_path)

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

if __name__ == "__main__":
    # Генерація даних для нового клієнта
    fake_client_data = generate_fake_client_data()
    user_data = pd.DataFrame([fake_client_data])


    # Передбачення
    result = predict(user_data)
    print("Результати з повних даних:", result)

    # Генерація неповних даних, для перевірки як модель справляється з обробкою
    corrupt_client_data = generate_and_corrupt_data()
    corrupt_user_data = pd.DataFrame([corrupt_client_data])

    # Передбачення
    result = predict(corrupt_user_data)
    print("Результати з неповних даних:", result)