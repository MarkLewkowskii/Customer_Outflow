import random

def generate_high_risk_client_data():
    """
    Генерує фейкові дані для клієнта з високою ймовірністю відтоку.

    :return: Словник із згенерованими даними клієнта.
    """
    high_risk_data = {
        "is_tv_subscriber": random.choice([0, 1]),
        "is_movie_package_subscriber": random.choice([0, 1]),
        "subscription_age": round(random.uniform(0.1, 12.0), 2),  # Короткий термін підписки
        "bill_avg": round(random.uniform(100, 200), 2),  # Високі рахунки
        "reamining_contract": round(random.uniform(0, 3), 2),  # Майже без залишкового контракту
        "service_failure_count": random.randint(5, 10),  # Часті збої
        "download_avg": round(random.uniform(70, 100), 1),  # Високе завантаження
        "upload_avg": round(random.uniform(30, 50), 1),  # Високе вивантаження
        "download_over_limit": 1  # Перевищення ліміту завантаження
    }
    return high_risk_data

def generate_fake_client_data(high_risk_probability=0.7):
    """
    Генерує фейкові дані для клієнта, з високою ймовірністю відтоку для певного відсотка.

    :param high_risk_probability: Ймовірність генерації даних високого ризику.
    :return: Словник із згенерованими даними клієнта.
    """
    if random.random() < high_risk_probability:
        return generate_high_risk_client_data()
    else:
        return {
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
