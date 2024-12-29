import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

# Завантаження датасету
df = pd.read_csv("data/raw/internet_service_churn.csv")
target_columns = ['subscription_age', 'bill_avg', 'reamining_contract', 'download_avg', 'upload_avg']

# scaler
scaler = StandardScaler()
scaler.fit(df[target_columns])

# Збереження
joblib.dump(scaler, "data/processed/scaler.pkl")

print("Файл scaler.pkl створено")
