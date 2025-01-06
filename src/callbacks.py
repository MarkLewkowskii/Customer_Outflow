import os
import json
import pandas as pd
import plotly.express as px
from dash import Input, Output, State, html
from joblib import load
from model_training import predict
from faker_new_client import generate_fake_client_data

# Ініціалізація глобальних змінних
all_predictions = []

def get_results_path(filename="model_evaluation.json"):
    """
    Функція для отримання шляху до файлу результатів.
    """
    root_path = os.getcwd()
    results_path = os.path.join(root_path, "results", filename)
    if not os.path.exists(results_path):
        raise FileNotFoundError(f"Файл результатів {results_path} не знайдено.")
    return results_path

def categorize_risk(probability):
    """Категоризація ризику за ймовірністю."""
    if probability < 20:
        return "Низький ризик", "green"
    elif probability < 50:
        return "Середній ризик", "orange"
    else:
        return "Високий ризик", "red"

def register_callbacks(app):
    """Реєстрація callback-функцій."""
    global all_predictions

    @app.callback(
        [Output("subscription-age", "value"),
         Output("bill-avg", "value"),
         Output("reamining_contract", "value"),
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
        fake_data = generate_fake_client_data(high_risk_probability=0.7)
        return [
            fake_data.get("subscription_age"),
            fake_data.get("bill_avg"),
            fake_data.get("reamining_contract"),
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
        [State("model-selector", "value"),
         State("subscription-age", "value"),
         State("bill-avg", "value"),
         State("reamining_contract", "value"),
         State("download-avg", "value"),
         State("upload-avg", "value"),
         State("service-failure-count", "value"),
         State("is-tv-subscriber", "value"),
         State("is-movie-package", "value"),
         State("download-over-limit", "value")]
    )
    def update_cards(n_clicks, model_name, subscription_age, bill_avg, reamining_contract,
                download_avg, upload_avg, service_failure_count,
                is_tv, is_movie, over_limit):
        if n_clicks is None:
            return "N/A", {"color": "#000"}, "N/A", "0", "0%"

        # Перевірка на None
        if any(v is None for v in [subscription_age, bill_avg, reamining_contract,
                               download_avg, upload_avg, service_failure_count,
                               is_tv, is_movie, over_limit]):
            return "Incomplete Data", {"color": "#000"}, "Incomplete Data", "0", "0%"

        try:
            input_data = {
                "is_tv_subscriber": is_tv,
                "is_movie_package_subscriber": is_movie,
                "subscription_age": subscription_age,
                "bill_avg": bill_avg,
                "reamining_contract": reamining_contract,
                "service_failure_count": service_failure_count,
                "download_avg": download_avg,
                "upload_avg": upload_avg,
                "download_over_limit": over_limit
            }
            input_df = pd.DataFrame([input_data])
            prediction = predict(input_df, model_name)
            probability = prediction['probability_of_churn'][0]
            risk_label, color = categorize_risk(probability)

            all_predictions.append(probability)
            average_churn = sum(all_predictions) / len(all_predictions)

            return risk_label, {"color": color}, f"{probability:.2f}%", str(len(all_predictions)), f"{average_churn:.2f}%"

        except Exception as e:
            return f"Error: {str(e)}", {"color": "#000"}, "Error", "0", "0%"

    @app.callback(
        Output("model-comparison-chart", "figure"),
        Input("predict-button", "n_clicks")
    )
    def update_model_chart(n_clicks):
        try:
            # Завантаження даних з JSON
            result_path = get_results_path("model_evaluation.json")

            with open(result_path) as f:
                model_data = json.load(f)

            print("JSON дані успішно завантажені:", model_data)

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

                # Додавання метрик, лише якщо вони присутні
                if "accuracy" in classification_report:
                    data.append({
                        "Model": abbreviated_name,
                        "Metric": "Accuracy",
                        "Value": classification_report["accuracy"]
                    })
                if "model_size_mb" in metrics:
                    data.append({
                        "Model": abbreviated_name,
                        "Metric": "Model Size (MB)",
                        "Value": metrics["model_size_mb"]
                    })
                if "macro avg" in classification_report:
                    macro_avg = classification_report["macro avg"]
                    data.append({
                        "Model": abbreviated_name,
                        "Metric": "Precision",
                        "Value": macro_avg.get("precision", 0)
                    })
                    data.append({
                        "Model": abbreviated_name,
                        "Metric": "Recall",
                        "Value": macro_avg.get("recall", 0)
                    })

            # Перетворення у DataFrame
            df = pd.DataFrame(data)

            # Додавання debug print для перевірки даних
            print("Data for plot:", df)

            # Побудова графіка
            fig = px.bar(
                df,
                x="Model",
                y="Value",
                color="Metric",
                barmode="group",
                template="plotly_white",
                labels={"Value": "Metric Value", "Model": "Models"}
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
                xaxis_title="Models",
                yaxis_title="Metric Value",
                legend_title="Metrics",
                xaxis_tickangle=-45,
                bargap=0.15  # Відстань між групами барів
            )

            return fig

        except FileNotFoundError as e:
            print(f"Файл не знайдено: {e}")
            return px.bar(title="Файл результатів не знайдено.")
        except json.JSONDecodeError as e:
            print(f"Помилка декодування JSON: {e}")
            return px.bar(title="Помилка декодування JSON")
        except Exception as e:
            print(f"Невідома помилка: {e}")
            return px.bar(title=f"Помилка: {e}")

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

        # Додавання debug print для перевірки даних
        print("History data for plot:", history_df)

        fig = px.line(
            history_df,
            x="Ітерація",
            y="Ймовірність відтоку (%)",
            markers=True,
            title="Історія прогнозів",
        )

        fig.update_layout(
            xaxis_title="Ітерація",
            yaxis_title="Ймовірність відтоку (%)",
            template="plotly_white",
            xaxis=dict(tickmode="linear"),
        )

        return fig