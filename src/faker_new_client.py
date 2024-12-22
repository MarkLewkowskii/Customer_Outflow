"""
[UKR] Скріпт генерації фейкових даних нового клієнта для подальшого підставляння їх у скріп "прогнозування нового клієнта"
[ENG] A script for generating fake data of a new client for further substituting them in the "prediction of a new client" script
"""

import pandas as pd
from faker import Faker

def generate_fake_client_data(num_customers):
    """
    Генерує фейкові дані клієнтів на основі заданої кількості.

    Args:
        num_customers: Кількість клієнтів, які потрібно згенерувати.

    Returns:
        pandas.DataFrame: DataFrame з фейковими даними.
    """

    fake = Faker()

    # пустий DataFrame з потрібними колонками
    columns = ['id', 'is_tv_subscriber', 'is_movie_package_subscriber', 'subscription_age',
               'bill_avg', 'reamining_contract', 'service_failure_count', 'download_avg',
               'upload_avg', 'download_over_limit', 'churn']
    data = []

    # Генеруємо дані
    for _ in range(num_customers):
        new_row = {
            'id': fake.uuid4(),
            'is_tv_subscriber': fake.boolean(),
            'is_movie_package_subscriber': fake.boolean(),
            'subscription_age': fake.random_int(min=1, max=120),
            'bill_avg': fake.random_int(min=20, max=200),
            'reamining_contract': fake.random_int(min=0, max=24),
            'service_failure_count': fake.random_int(min=0, max=5),
            'download_avg': fake.random_int(min=10, max=100),
            'upload_avg': fake.random_int(min=5, max=50),
            'download_over_limit': fake.boolean(),
            'churn': fake.boolean()
        }
        data.append(new_row)

    return pd.DataFrame(data)
