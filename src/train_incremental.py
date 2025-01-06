import os
from joblib import load, dump
import pandas as pd
from shared import SUPPORTED_INCREMENTAL_MODELS, BASE_DIR, MODEL_PATHS, NEW_DATA_PATH


def load_new_data(data_path):
    """
    Завантажує нові дані для донавчання.
    Перевіряє наявність файлу та непорожність даних.
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Файл з новими даними {data_path} не знайдено.")

    print(f"Завантаження нових даних з {data_path}...")
    data = pd.read_csv(data_path)

    if data.empty:
        raise ValueError(f"Файл {data_path} не містить даних.")

    return data


def train_incremental_model(model_name, new_data):
    """
    Функція для донавчання моделі.
    :param model_name: Назва моделі.
    :param new_data: DataFrame із новими даними.
    """
    if model_name not in SUPPORTED_INCREMENTAL_MODELS:
        print(f"Модель {model_name} не підтримує донавчання.")
        return

    model_path = MODEL_PATHS.get(model_name)
    if not model_path or not os.path.exists(model_path):
        print(f"Модель {model_name} не знайдено за шляхом {model_path}.")
        return

    # Завантаження моделі
    model = load(model_path)

    # Розділення даних на X і y
    X = new_data.drop(columns=["churn"], errors="ignore")
    y = new_data["churn"]

    # Виконання partial_fit для моделей, які підтримують донавчання
    try:
        model.partial_fit(X, y, classes=[0, 1])
        # Збереження оновленої моделі
        dump(model, model_path)
        print(f"Модель {model_name} успішно донавчена й збережена.")
    except Exception as e:
        print(f"Помилка під час донавчання моделі {model_name}: {e}")


def get_incremental_models():
    """
    Фільтрує моделі, які підтримують донавчання.
    :return: Словник моделей для донавчання.
    """
    return {k: v for k, v in MODEL_PATHS.items() if k in SUPPORTED_INCREMENTAL_MODELS}


def main():
    """
    Основна функція для донавчання моделей.
    """
    try:
        os.makedirs(os.path.dirname(NEW_DATA_PATH), exist_ok=True)

        # Завантаження нових даних
        new_data = load_new_data(NEW_DATA_PATH)
        print(f"Нові дані завантажено. Розмір: {new_data.shape}")

        # Отримання моделей, які підтримують донавчання
        incremental_models = get_incremental_models()
        if not incremental_models:
            print("Немає моделей, які підтримують донавчання.")
            return

        # Донавчання кожної моделі
        for model_name, model_path in incremental_models.items():
            print(f"Донавчання моделі {model_name}...")
            train_incremental_model(model_name, new_data)
            print(f"Модель {model_name} успішно донавчена.")

    except FileNotFoundError as e:
        print(f"Файл не знайдено: {e}")
    except ValueError as e:
        print(f"Помилка у даних: {e}")
    except Exception as e:
        print(f"Сталася непередбачена помилка: {e}")


if __name__ == "__main__":
    main()
