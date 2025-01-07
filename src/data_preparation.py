import json
import joblib
import pandas as pd
def preprocess_user_data(data: pd.DataFrame, scaler_path: str) -> pd.DataFrame:
    """
    Обробляє дані користувача для моделі з використанням медіан і StandardScaler.

    :param data: DataFrame з даними користувача.
    :param scaler_path: Шлях до моделі StandardScaler для масштабування числових даних.
    :return: Оброблений DataFrame.
    """
    # Числові та категоріальні ознаки
    numerical_columns = ['subscription_age', 'bill_avg', 'remaining_contract', 
                         'download_avg', 'upload_avg']

    # Масштабування числових змінних
    scaler = joblib.load(scaler_path)
    data[numerical_columns] = scaler.transform(data[numerical_columns])

    return data
