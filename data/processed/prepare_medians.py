import pandas as pd
import json

# Завантаження датасету
df = pd.read_csv("data/raw/internet_service_churn.csv")
target_columns = ['subscription_age', 'bill_avg', 'reamining_contract', 'download_avg', 'upload_avg']

# Обчислення медіан
medians = df[target_columns].median(numeric_only=True).to_dict()

# Збереження медіан у файл
with open("data/processed/medians.json", "w") as f:
    json.dump(medians, f)

print("Файл medians.json створено")