from faker import Faker
import random
import pandas as pd
from shared import EXPECTED_COLUMNS

fake = Faker()

def generate_fake_client_data() -> dict:
    """
    Генерує фейкові дані для нового клієнта.

    :return: Словник із згенерованими даними клієнта.
        - is_tv_subscriber: Вказує на підписку на ТБ (1 або 0).
        - is_movie_package_subscriber: Вказує на підписку на пакет фільмів (1 або 0).
        - subscription_age: Тривалість підписки в місяцях (float).
        - bill_avg: Середній розмір рахунку (float).
        - remaining_contract: Залишок контракту в місяцях (float, 0 якщо контракту немає).
        - service_failure_count: Кількість збоїв у сервісі (int).
        - download_avg: Середня швидкість завантаження в Мбіт/с (float).
        - upload_avg: Середня швидкість вивантаження в Мбіт/с (float).
        - download_over_limit: Вказує на перевищення ліміту завантаження (1 або 0).
    """
    fake_data = {
        "is_tv_subscriber": random.choice([0, 1]),
        "is_movie_package_subscriber": random.choice([0, 1]),
        "subscription_age": round(random.uniform(0.1, 120.0), 2),
        "bill_avg": round(random.uniform(0, 200), 2),
        "remaining_contract": round(random.uniform(0, 24), 2) if random.random() > 0.3 else 0,
        "service_failure_count": random.randint(0, 10),
        "download_avg": round(random.uniform(0, 100), 1),
        "upload_avg": round(random.uniform(0, 50), 1),
        "download_over_limit": random.choice([0, 1])
    }

    return fake_data

def generate_and_corrupt_data(corruption_rate: float = 0.3) -> dict:
    """
    Генерує фейкові дані клієнта, а потім псує їх із заданою ймовірністю.

    :param corruption_rate: Ймовірність видалення кожного ключа.
    :return: Зіпсовані дані клієнта.
    """
    fake_data = generate_fake_client_data()  # Генерація фейкових даних
    corrupted_data = fake_data.copy()
    for key in list(corrupted_data.keys()):
        if random.random() < corruption_rate:
            corrupted_data[key] = None  # Видаляємо значення
    return corrupted_data

def generate_test_data(num_samples: int, corruption_rate: float = 0.1) -> pd.DataFrame:
    """
    Генерує тестові дані для моделі з можливістю псування.

    :param num_samples: Кількість зразків для генерації.
    :param corruption_rate: Ймовірність псування даних.
    :return: DataFrame із згенерованими тестовими даними.
    """
    test_data = []
    for _ in range(num_samples):
        client_data = generate_fake_client_data()  # Генерація фейкових даних
        if random.random() < corruption_rate:
            client_data = generate_and_corrupt_data(corruption_rate)  # Псування даних
        test_data.append(client_data)

    # Створення DataFrame і забезпечення наявності всіх EXPECTED_COLUMNS
    df = pd.DataFrame(test_data)
    for column in EXPECTED_COLUMNS:
        if column not in df.columns:
            df[column] = 0  # Додаємо відсутні колонки з нульовим значенням
    return df
