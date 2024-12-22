"""
[ENG] Model testing module
[UKR] Модуль тестуваня моделі
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.preprocessing import LabelEncoder
from src.faker_new_client import generate_fake_client_data  # Assuming this function exists elsewhere

def preprocess_data(data):
    """
    [ENG] Preprocesses the dataset for training.
    [UKR] Передобробляє дані для тренування.

    Args:
        data (pd.DataFrame): The input dataset.

    Returns:
        pd.DataFrame, pd.Series: Processed features and target variable.
    """
    # Convert categorical columns to numeric using LabelEncoder
    le = LabelEncoder()
    for col in data.select_dtypes(include=['object', 'bool']).columns:
        data[col] = le.fit_transform(data[col])

    # Separate features and target
    X = data.drop('churn', axis=1)
    y = data['churn']
    return X, y

def test_model_performance():
    """
    [ENG] This function trains a churn prediction model, evaluates its performance on a testing set,
    and prints the results.
    [UKR] Ця функція навчає модель прогнозування відтоку, оцінює її продуктивність на наборі для тестування,
    і друкує результати.
    """
    # Load real data
    data = pd.read_csv('customers.csv')

    # Generate fake data and concatenate
    fake_data = generate_fake_client_data(1000)
    data = pd.concat([data, fake_data], ignore_index=True)

    # Preprocess data
    X, y = preprocess_data(data)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Make predictions on the testing set
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]  # Probabilities for ROC-AUC

    # Evaluate model performance
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)

    # Print results
    print("Model Performance:")
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1-score:", f1)
    print("AUC:", auc)

# Run the test
test_model_performance()
