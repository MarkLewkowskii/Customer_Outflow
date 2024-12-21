'''
[UKR] Скріпт генерації фейкових даних нового клієнта для подальшого підставляння їх у скріп "прогнозування нового клієнта"
[ENG] A script for generating fake data of a new client for further substituting them in the "prediction of a new client" script
'''


from faker import Faker
import random

fake = Faker()

def generate_fake_client_data():
    """
    Генерує фейкові дані нового клієнта.

    :return: Словник із згенерованими даними клієнта.
        - age: Вік клієнта (int).
        - monthly_charges: Щомісячні витрати клієнта (float).
        - tenure: Термін обслуговування у місяцях (int).
        - dependents: Наявність утриманців (0 - немає, 1 - є).

    :doc-author: kagev
    """

    fake_data = {
        "age": random.randint(18, 85),  # Вік клієнта
        "monthly_charges": round(random.uniform(20, 150), 2),  # Щомісячні витрати
        "tenure": random.randint(1, 72),  # Термін обслуговування у місяцях
        "dependents": random.choice([0, 1])  # Наявність утриманців (0 - немає, 1 - є)
    }
    return fake_data
