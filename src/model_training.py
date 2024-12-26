import pandas as pd
import joblib
from data_preparation import preprocess_user_data

# Шлях до збереженої моделі
model_path = "models/saved_model.pkl"

# Шляхи до медіан і scaler
medians_path = "data/processed/medians.json"
scaler_path = "data/processed/scaler.pkl"

def predict(data: pd.DataFrame) -> pd.DataFrame:
    """
    Здійснює передбачення на основі підготовлених даних і збереженої моделі.
    
    Параметри:
        data (pd.DataFrame): Сирі дані, отримані від користувача.
        
    Повертає:
        pd.DataFrame: Результати передбачення.
    """
    # Завантаження моделі
    model = joblib.load(model_path)
    
    # Попередня обробка даних
    processed_data = preprocess_user_data(data, medians_path, scaler_path)
    
    # Здійснення передбачення
    predictions = model.predict(processed_data)
    
    # Додавання передбачень до даних
    data['prediction'] = predictions
    
    return data

if __name__ == "__main__":
    # Приклад сирих даних
    user_data = pd.DataFrame({
        'subscription_age': [12],
        'bill_avg': [50],
        'reamining_contract': [None],  # Пропуск
        'download_avg': [75],
        'upload_avg': [None],  # Пропуск
        'is_tv_subscriber': [1],
        'is_movie_package_subscriber': [0],
        'download_over_limit': [0],
        'churn': [0]
    })
    
    # Передбачення
    result = predict(user_data)
    print(result)
