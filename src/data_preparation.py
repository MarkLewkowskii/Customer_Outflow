import os

import pandas as pd
import json
from sklearn.preprocessing import StandardScaler
from joblib import load
from shared import EXPECTED_COLUMNS, PROCESSED_DIR


def preprocess_user_data(data: pd.DataFrame, medians_path: str, scaler_path: str) -> pd.DataFrame:
    """
    Обробляє дані користувача для моделі з використанням медіан і StandardScaler.

    :param data: DataFrame з даними користувача.
    :param medians_path: Шлях до JSON файлу з медіанами для заповнення пропусків.
    :param scaler_path: Шлях до моделі StandardScaler для масштабування числових даних.
    :return: Оброблений DataFrame.
    """

    # Завантаження медіан
    with open(medians_path, "r") as f:
        medians = json.load(f)

    # Розділення на числові та категоріальні ознаки
    numerical_columns = ['subscription_age', 'bill_avg', 'remaining_contract',
                         'download_avg', 'upload_avg']
    categorical_columns = ['is_tv_subscriber', 'is_movie_package_subscriber',
                           'download_over_limit', 'service_failure_count']

    # Заповнення пропусків у числових колонках
    for column in numerical_columns:
        if column in data.columns:
            data[column] = data[column].fillna(medians.get(column, 0))

    # Масштабування числових колонок
    scaler = load(scaler_path)
    data[numerical_columns] = scaler.transform(data[numerical_columns])

    # Повертаємо тільки очікувані колонки
    return data[EXPECTED_COLUMNS]


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

    # Визначення числових колонок
    numerical_columns = [
        "subscription_age", "bill_avg", "remaining_contract",
        "download_avg", "upload_avg", "service_failure_count"
    ]

    # Заповнення пропусків у числових колонках
    for column in numerical_columns:
        if column in data.columns:
            data[column] = data[column].fillna(medians.get(column, 0))

    # Завантаження scaler і перевірка відповідності колонок
    scaler = load(scaler_path)
    scaler_feature_names_path = os.path.join(PROCESSED_DIR, "scaler_feature_names.json")

    # Завантажуємо список колонок, які використовувалися для `scaler.fit`
    if not os.path.exists(scaler_feature_names_path):
        raise FileNotFoundError(f"Файл {scaler_feature_names_path} не знайдено. Спочатку навчіть scaler.")

    with open(scaler_feature_names_path, "r") as f:
        scaler_feature_names = json.load(f)

    # Перевірка на відповідність колонок
    if numerical_columns != scaler_feature_names:
        raise ValueError(f"Колонки у вхідних даних не відповідають колонкам, використаним для scaler.fit: {scaler_feature_names}")

    # Масштабування даних
    data[numerical_columns] = scaler.transform(data[scaler_feature_names])

    return data


def ensure_columns(data: pd.DataFrame, expected_columns: list) -> pd.DataFrame:
    """
    Гарантує, що всі очікувані колонки присутні у DataFrame. Додає відсутні колонки із значенням 0.

    :param data: DataFrame для перевірки.
    :param expected_columns: Список очікуваних колонок.
    :return: DataFrame із усіма очікуваними колонками.
    """
    for column in expected_columns:
        if column not in data.columns:
            data[column] = 0
    return data
