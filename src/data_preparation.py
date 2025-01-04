import json
import joblib
import pandas as pd

def preprocess_user_data(data: pd.DataFrame, medians_path: str, scaler_path: str) -> pd.DataFrame:
    """
    Обробляє дані користувача для моделі з використанням медіан і StandardScaler.

    :param data: DataFrame з даними користувача.
    :param medians_path: Шлях до JSON файлу з медіанами для заповнення пропусків.
    :param scaler_path: Шлях до моделі StandardScaler для масштабування числових даних.
    :return: Оброблений DataFrame.
    """

    # Завантаження медіан
    with open(medians_path, 'r') as file:
        medians = json.load(file)

    # Числові та категоріальні ознаки
    numerical_columns = ['subscription_age', 'bill_avg', 'remaining_contract', 
                         'download_avg', 'upload_avg']
    categorical_columns = ['is_tv_subscriber', 'is_movie_package_subscriber', 
                           'service_failure_count', 'download_over_limit']

    # Заповнення пропусків у числових колонках
    for column in numerical_columns:
        if column in data.columns:
            if data[column].dtype.kind in 'bifc':  # Перевірка числового типу
                data[column] = data[column].fillna(medians.get(column, 0))
            else:
                raise TypeError(f"Колонка {column} не є числовою. Поточний тип: {data[column].dtype}")
        else:
            data[column] = medians.get(column, 0)  # Додаємо відсутні стовпці

    # Заповнення пропусків у категоріальних колонках
    for column in categorical_columns:
        if column not in data.columns:
            data[column] = 0  # Додаємо відсутні стовпці

    # Масштабування числових змінних
    scaler = joblib.load(scaler_path)
    data[numerical_columns] = scaler.transform(data[numerical_columns])

    return data

