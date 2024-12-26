import pandas as pd
import json
import joblib
from sklearn.preprocessing import StandardScaler

def preprocess_user_data(data: pd.DataFrame, medians_path: str, scaler_path: str) -> pd.DataFrame:
    """
    Обробляє дані користувача для моделі з використанням медіан і StandardScaler.

    Параметри:
        data (pd.DataFrame): Набір даних, отриманий від користувача.
        medians_path (str): Шлях до JSON-файлу з медіанами.
        scaler_path (str): Шлях до файлу з параметрами StandardScaler.

    Повертає:
        pd.DataFrame: Оброблений набір даних.
    """
    # Завантаження медіан
    with open(medians_path, 'r') as file:
        medians = json.load(file)

    # Заповнення пропусків медіанами
    for column, median_value in medians.items():
        if column in data.columns:
            data[column].fillna(median_value, inplace=True)

    # Завантаження збереженого StandardScaler
    scaler = joblib.load(scaler_path)
    numerical_columns = ['subscription_age', 'bill_avg', 'reamining_contract', 'download_avg', 'upload_avg']

    # Масштабування числових змінних
    if all(col in data.columns for col in numerical_columns):
        data[numerical_columns] = scaler.transform(data[numerical_columns])
    else:
        raise ValueError(f"Одна або більше числових змінних відсутні: {numerical_columns}")

    return data
