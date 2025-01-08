import os
import json
import pandas as pd
import plotly.express as px
from dash import Input, Output, State
from joblib import dump, load
from faker_new_client import generate_fake_client_data
from shared import SUPPORTED_INCREMENTAL_MODELS, MODEL_PATHS, EVALUATION_RESULTS_PATH
from model_training import predict
from train_incremental import train_incremental_model


# Ініціалізація глобальних змінних
all_predictions = []


def standardize_and_predict(data, model_path):
    """
    Функція для стандартизації введених даних.
    """
    try:
        standardized_data = pd.DataFrame({
            "is_tv_subscriber": [int(data.get("is_tv", 0))],
            "is_movie_package_subscriber": [int(data.get("is_movie", 0))],
            "subscription_age": [float(data.get("subscription_age", 0))],
            "bill_avg": [float(data.get("bill_avg", 0))],
            "remaining_contract": [float(data.get("remaining_contract", 0))],
            "service_failure_count": [int(data.get("service_failure_count", 0))],
            "download_avg": [float(data.get("download_avg", 0))],
            "upload_avg": [float(data.get("upload_avg", 0))],
            "download_over_limit": [int(data.get("download_over_limit", 0))]
        })
        return predict(standardized_data, model_path)
    except Exception as e:
        raise ValueError(f"Помилка при стандартизації даних: {e}")


def categorize_risk(probability):
    """
    Категоризація ризику за ймовірністю.
    """
    if probability < 30:
        return "Низький ризик", "green"  # Зелений
    elif 30 <= probability < 60:
        return "Середній ризик", "orange"  # Жовтий
    else:
        return "Високий ризик", "red"  # Червоний


def register_callbacks(app):
    """
    Реєстрація callback-функцій для Dash-додатку.
    """
    global all_predictions

    @app.callback(
        [Output("subscription-age", "value"),
         Output("bill-avg", "value"),
         Output("remaining-contract", "value"),
         Output("download-avg", "value"),
         Output("upload-avg", "value"),
         Output("service-failure-count", "value"),
         Output("is-tv-subscriber", "value"),
         Output("is-movie-package", "value"),
         Output("download-over-limit", "value")],
        [Input("random-button", "n_clicks")]
    )
    def fill_random_data(n_clicks):
        if n_clicks is None:
            return [None] * 9
        fake_data = generate_fake_client_data()
        return [
            fake_data.get("subscription_age"),
            fake_data.get("bill_avg"),
            fake_data.get("remaining_contract"),
            fake_data.get("download_avg"),
            fake_data.get("upload_avg"),
            fake_data.get("service_failure_count"),
            fake_data.get("is_tv_subscriber"),
            fake_data.get("is_movie_package_subscriber"),
            fake_data.get("download_over_limit")
        ]

    @app.callback(
        [Output("risk-output", "children"),
         Output("risk-output", "style"),
         Output("churn-probability-output", "children"),
         Output("total-predictions-output", "children"),
         Output("average-churn-output", "children")],
        [Input("predict-button", "n_clicks")],
        [
            State("model-selector", "value"),
            State("subscription-age", "value"),
            State("bill-avg", "value"),
            State("remaining-contract", "value"),
            State("download-avg", "value"),
            State("upload-avg", "value"),
            State("service-failure-count", "value"),
            State("is-tv-subscriber", "value"),
            State("is-movie-package", "value"),
            State("download-over-limit", "value")
        ]
    )
    def make_prediction(n_clicks, model_name, subscription_age, bill_avg, remaining_contract,
                        download_avg, upload_avg, service_failure_count,
                        is_tv, is_movie, over_limit):
        if n_clicks is None:
            return "N/A", {"color": "#000"}, "N/A", "0", "0%"

        if any(v is None for v in [subscription_age, bill_avg, remaining_contract,
                                   download_avg, upload_avg, service_failure_count,
                                   is_tv, is_movie, over_limit]):
            return "Incomplete Data", {"color": "#000"}, "Incomplete Data", "0", "0%"

        try:
            model_path = MODEL_PATHS.get(model_name)
            if not model_path:
                return "Модель не знайдена", {"color": "#000"}, "Error", "0", "0%"

            model = load(model_path)

            input_data = pd.DataFrame({
                "is_tv_subscriber": [int(is_tv)],
                "is_movie_package_subscriber": [int(is_movie)],
                "subscription_age": [float(subscription_age)],
                "bill_avg": [float(bill_avg)],
                "remaining_contract": [float(remaining_contract)],
                "service_failure_count": [int(service_failure_count)],
                "download_avg": [float(download_avg)],
                "upload_avg": [float(upload_avg)],
                "download_over_limit": [int(over_limit)],
            })

            result = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1] * 100

            risk_label, color = categorize_risk(probability)

            all_predictions.append(probability)
            average_churn = sum(all_predictions) / len(all_predictions)

            return risk_label, {"color": color}, f"{probability:.2f}%", str(len(all_predictions)), f"{average_churn:.2f}%"

        except Exception as e:
            print(f"Помилка: {e}")
            return "Error", {"color": "#000"}, "Error", "0", "0%"

    @app.callback(
        Output("history-graph", "figure"),
        Input("predict-button", "n_clicks")
    )
    def update_history_graph(n_clicks):
        if not all_predictions:
            return px.line(title="Історія прогнозів")

        history_df = pd.DataFrame({
            "Ітерація": list(range(1, len(all_predictions) + 1)),
            "Ймовірність відтоку (%)": all_predictions
        })

        fig = px.line(
            history_df,
            x="Ітерація",
            y="Ймовірність відтоку (%)",
            markers=True,
            title="Історія прогнозів"
        )

        fig.update_layout(
            xaxis_title="Ітерація",
            yaxis_title="Ймовірність відтоку (%)",
            template="plotly_white"
        )

        return fig

    @app.callback(
        [
            Output("input-subscription-age", "children"),
            Output("input-bill-avg", "children"),
            Output("input-remaining-contract", "children"),
            Output("input-download-avg", "children"),
            Output("input-upload-avg", "children"),
            Output("input-service-failure-count", "children"),
            Output("input-tv-subscriber", "children"),
            Output("input-movie-package", "children"),
            Output("input-over-limit", "children"),
        ],
        [Input("predict-button", "n_clicks")],
        [
            State("subscription-age", "value"),
            State("bill-avg", "value"),
            State("remaining-contract", "value"),
            State("download-avg", "value"),
            State("upload-avg", "value"),
            State("service-failure-count", "value"),
            State("is-tv-subscriber", "value"),
            State("is-movie-package", "value"),
            State("download-over-limit", "value"),
        ]
    )
    def update_table(n_clicks, *values):
        if n_clicks is None:
            return ["—"] * len(values)

        boolean_to_text = lambda x: "Так" if x == 1 else "Ні"
        return [
            values[0] or "—",
            values[1] or "—",
            values[2] or "—",
            values[3] or "—",
            values[4] or "—",
            values[5] or "—",
            boolean_to_text(values[6]),
            boolean_to_text(values[7]),
            boolean_to_text(values[8]),
        ]

    @app.callback(
        Output("model-comparison-chart", "figure"),
        Input("predict-button", "n_clicks")
    )
    def update_model_chart(n_clicks):
        try:
            # Завантаження даних з JSON
            result_path = EVALUATION_RESULTS_PATH

            with open(result_path) as f:
                model_data = json.load(f)

            # print("JSON дані успішно завантажені:", model_data)

            # Структурування даних
            data = []

            # Абревіатури для моделей
            abbreviations = {
                "Histogram-based Gradient Boosting Classification Tree": "HGBCT",
                "Random Forest": "RF",
                "Gradient Boosting": "GB",
                "Logistic Regression": "LR"
            }

            for model_name, metrics in model_data.items():
                classification_report = metrics.get("classification_report", {})
                abbreviated_name = abbreviations.get(model_name, model_name)

                # Додавання accuracy
                if "accuracy" in classification_report:
                    data.append({
                        "Model": abbreviated_name,
                        "Metric": "Accuracy",
                        "Value": classification_report["accuracy"]
                    })

                # Додавання model size
                if "model_size_mb" in metrics:
                    data.append({
                        "Model": abbreviated_name,
                        "Metric": "Model Size (MB)",
                        "Value": metrics["model_size_mb"]
                    })

                # Додавання macro avg precision
                if "macro avg" in classification_report:
                    macro_avg = classification_report["macro avg"]
                    data.append({
                        "Model": abbreviated_name,
                        "Metric": "Macro Avg Precision",
                        "Value": macro_avg.get("precision", 0)
                    })

                # Додавання weighted avg precision
                if "weighted avg" in classification_report:
                    weighted_avg = classification_report["weighted avg"]
                    data.append({
                        "Model": abbreviated_name,
                        "Metric": "Weighted Avg Precision",
                        "Value": weighted_avg.get("precision", 0)
                    })

                # Перетворення у DataFrame
            df = pd.DataFrame(data)

            # Побудова графіка
            fig = px.bar(
                df,
                x="Metric",
                y="Value",
                color="Model",
                barmode="group",
                template="plotly_white",
                labels={"Value": "Metric Value", "Metric": "Metrics"}
            )

            # Додавання підписів до барів
            fig.update_traces(
                text=df["Value"].round(3),
                textposition='outside',
                marker=dict(line=dict(width=1.5, color='black'))
            )

            # Покращення дизайну
            fig.update_layout(
                title_font=dict(size=20, family='Arial'),
                xaxis_title="Metrics",
                yaxis_title="Metric Value",
                legend_title="Models",
                xaxis_tickangle=-45,
                bargap=0.15  # Відстань між групами барів
            )

            return fig

        except FileNotFoundError as e:
            print(f"Файл не знайдено: {e}")
            return px.bar(title="Файл model_evaluation.json не знайдено")
        except Exception as e:
            print(f"Помилка під час створення графіка: {e}")
            return px.bar(title="Помилка під час створення графіка")