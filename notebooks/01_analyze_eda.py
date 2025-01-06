import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Завантаження даних
file_path = 'data/raw/internet_service_churn.csv'
data = pd.read_csv(file_path)

# Заміна значень `inf` і `-inf` на `NaN`
data = data.replace([float('inf'), float('-inf')], pd.NA)

# Аналіз пропущених значень
missing_values = data.isnull().sum()
missing_percentage = (missing_values / len(data)) * 100
missing_report = pd.DataFrame({'Відсутні значення': missing_values, '% Пропусків': missing_percentage})

# Графіки
output_dir = "results/visualizations"
os.makedirs(output_dir, exist_ok=True)

# Гістограми
numeric_columns = ['subscription_age', 'bill_avg', 'remaining_contract',
                   'service_failure_count', 'download_avg', 'upload_avg']

plt.figure(figsize=(15, 10))
for i, column in enumerate(numeric_columns, 1):
    plt.subplot(2, 3, i)
    sns.histplot(data[column], kde=True, bins=30, color='skyblue')
    plt.title(f'Розподіл {column}')
plt.tight_layout()
plt.savefig(f"{output_dir}/histograms.png")
plt.close()

# Коробкові графіки
plt.figure(figsize=(15, 10))
for i, column in enumerate(numeric_columns, 1):
    plt.subplot(2, 3, i)
    sns.boxplot(x=data[column], color='lightcoral')
    plt.title(f'Коробковий графік {column}')
plt.tight_layout()
plt.savefig(f"{output_dir}/boxplots.png")
plt.close()

# Кореляційна матриця
correlation_matrix = data[numeric_columns].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("Кореляційна матриця")
plt.savefig(f"{output_dir}/correlation_matrix.png")
plt.close()

# Збереження звіту
def save_report_to_file(filename, report_lines):
    with open(filename, "w", encoding="utf-8") as file:
        for line in report_lines:
            file.write(line + "\n")
    print(f"Звіт збережено у файл {filename}")

report_lines = [
    "1. Пропущені значення",
    missing_report.to_string(),
    "",
    "2. Візуалізації",
    "histograms.png: Розподіли числових змінних.",
    "boxplots.png: Коробкові графіки для виявлення викидів.",
    "correlation_matrix.png: Кореляційна матриця.",
    "",
    "3. Основні висновки",
    "Пропущені дані у змінній `remaining_contract` можуть впливати на точність аналізу.",
    "Сильна кореляція між `download_avg` та `upload_avg`.",
    "",
    "4. Рекомендації",
    "Імпутувати пропуски у змінній `remaining_contract` за допомогою медіани.",
    "Оптимізувати змінні `download_avg` та `upload_avg` через високу кореляцію."
]

save_report_to_file("results/summary_report.txt", report_lines)
