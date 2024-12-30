from faker import Faker
import random
import numpy as np

def generate_fake_client_data():
    """
    Генерує фейкові дані для нового клієнта.

    :return: Словник із згенерованими даними клієнта.
        - is_tv_subscriber: Вказує на підписку на ТБ (1 або 0).
        - is_movie_package_subscriber: Вказує на підписку на пакет фільмів (1 або 0).
        - subscription_age: Тривалість підписки в місяцях (float).
        - bill_avg: Середній розмір рахунку (float).
        - reamining_contract: Залишок контракту в місяцях (float, NaN якщо контракту немає).
        - service_failure_count: Кількість збоїв у сервісі (int).
        - download_avg: Середня швидкість завантаження в Мбіт/с (float).
        - upload_avg: Середня швидкість вивантаження в Мбіт/с (float).
        - download_over_limit: Вказує на перевищення ліміту завантаження (1 або 0).
    """
    fake = Faker()

    fake_data = {
        "is_tv_subscriber": random.choice([0, 1]),
        "is_movie_package_subscriber": random.choice([0, 1]),
        "subscription_age": round(random.uniform(0.1, 120.0), 2),
        "bill_avg": round(random.uniform(0, 200), 2),
        "reamining_contract": round(random.uniform(0, 24), 2) if random.random() > 0.3 else 0,
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
