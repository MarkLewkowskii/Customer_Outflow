import pandas as pd
import plotly.express as px
from dash import Input, Output, State, html
from joblib import load
from faker_new_client import generate_fake_client_data

# Глобальні змінні для збереження прогнозів
all_predictions = []

def prepare_input_data(subscription_age, bill_avg, remaining_contract,
                       download_avg, upload_avg, service_failure_count,
                       is_tv, is_movie, over_limit):
    """
    Підготовка вхідних даних у формат, який очікує модель.
    """
    return pd.DataFrame([{
        "subscription_age": subscription_age,
        "bill_avg": bill_avg,
        "remaining_contract": remaining_contract,
        "download_avg": download_avg,
        "upload_avg": upload_avg,
        "service_failure_count": service_failure_count,
        "is_tv_subscriber": is_tv,
        "is_movie_package_subscriber": is_movie,
        "download_over_limit": over_limit
    }])


def register_callbacks(app):
    # Callback для генерації випадкових даних
    @app.callback(
        [
            Output("subscription-age", "value"),
            Output("bill-avg", "value"),
            Output("remaining-contract", "value"),
            Output("download-avg", "value"),
            Output("upload-avg", "value"),
            Output("service-failure-count", "value"),
            Output("is-tv-subscriber", "value"),
            Output("is-movie-package", "value"),
            Output("download-over-limit", "value"),
        ],
        [Input("random-button", "n_clicks")]
    )
    def fill_random_data(n_clicks):
        if n_clicks is None:
            return [None] * 9  # Початкове значення
        fake_data = generate_fake_client_data()
        return [
            fake_data["subscription_age"],
            fake_data["bill_avg"],
            fake_data["remaining_contract"],  # Виправлено
            fake_data["download_avg"],
            fake_data["upload_avg"],
            fake_data["service_failure_count"],
            fake_data["is_tv_subscriber"],
            fake_data["is_movie_package_subscriber"],  # Виправлено
            fake_data["download_over_limit"],
        ]

    # Callback для оновлення таблиці
    @app.callback(
        [
            Output("subscription-age-display", "children"),
            Output("bill-avg-display", "children"),
            Output("remaining-contract-display", "children"),
            Output("download-avg-display", "children"),
            Output("upload-avg-display", "children"),
            Output("service-failure-count-display", "children"),
            Output("is-tv-subscriber-display", "children"),
            Output("is-movie-package-display", "children"),
            Output("download-over-limit-display", "children"),
            Output("risk-level-display-table", "children"),  # Для таблиці
            Output("probability-display-table", "children"),  # Для таблиці
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
    def update_table(n_clicks, subscription_age, bill_avg, remaining_contract,
                                download_avg, upload_avg, service_failure_count,
                                is_tv, is_movie, over_limit):
    # Якщо кнопка не натиснута
        if n_clicks is None:
            return ["-"] * 11

        # Підготовка даних для таблиці
        subscription_age_text = f"{subscription_age} місяців" if subscription_age else "-"
        bill_avg_text = f"{bill_avg} грн" if bill_avg else "-"
        remaining_contract_text = f"{remaining_contract} місяців" if remaining_contract else "-"
        download_avg_text = f"{download_avg} GB" if download_avg else "-"
        upload_avg_text = f"{upload_avg} GB" if upload_avg else "-"
        service_failure_count_text = f"{service_failure_count}" if service_failure_count else "-"
        is_tv_text = "Так" if is_tv == 1 else "Ні" if is_tv == 0 else "-"
        is_movie_text = "Так" if is_movie == 1 else "Ні" if is_movie == 0 else "-"
        over_limit_text = "Так" if over_limit == 1 else "Ні" if over_limit == 0 else "-"

        # Завантаження моделі
        model = load("models/model_RandomForest.joblib")
        input_data = prepare_input_data(subscription_age, bill_avg, remaining_contract,
                                        download_avg, upload_avg, service_failure_count,
                                        is_tv, is_movie, over_limit)
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1] * 100

        # Рівень ризику та ймовірність
        risk_level_text = "Високий" if prediction == 1 else "Низький"
        probability_text = f"{probability:.2f}%"

        return [
            subscription_age_text,
            bill_avg_text,
            remaining_contract_text,
            download_avg_text,
            upload_avg_text,
            service_failure_count_text,
            is_tv_text,
            is_movie_text,
            over_limit_text,
            risk_level_text,
            probability_text,
        ]

    # Callback для карт
    app.callback(
        [
            Output("risk-level-card", "children"),  # Для картки
            Output("probability-card", "children"),  # Для картки
            Output("prediction-count-card", "children"),  # Кількість прогнозів
            Output("average-risk-card", "children"),  # Середній відсоток відтоку
        ],
        [Input("predict-button", "n_clicks")]
    )

    def update_cards(n_clicks):
        global all_predictions

        if n_clicks is None or not all_predictions:
            return "-", "-", "0", "-"

        # Загальна кількість прогнозів
        total_predictions = len(all_predictions)

        # Середня ймовірність
        avg_probability = sum(p["Ймовірність відтоку (%)"] for p in all_predictions) / total_predictions

        # Поточний прогноз
        last_prediction = all_predictions[-1]
        current_risk_level = last_prediction["Рівень ризику"]
        current_probability = f"{last_prediction['Ймовірність відтоку (%)']:.2f}%"

        return (
            current_risk_level,
            current_probability,
            str(total_predictions),
            f"{avg_probability:.2f}%",
        )

    # Callback для прогнозу
    @app.callback(
        [
            Output("prediction-details", "children"),  # Деталі прогнозу
            Output("history-graph", "figure"),  # Графік історії прогнозів
        ],
        [Input("predict-button", "n_clicks")],  # Тригер на натискання кнопки
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
    def update_prediction_and_graph(
            n_clicks, subscription_age, bill_avg, remaining_contract,
            download_avg, upload_avg, service_failure_count,
            is_tv, is_movie, over_limit
    ):
        global all_predictions

        # Якщо кнопка не натиснута, повертаємо значення за замовчуванням
        if n_clicks is None:
            return "Введіть дані та натисніть кнопку для прогнозування", px.line(
                title="Історія прогнозів (немає даних)"
            )

        # Перевірка наявності всіх необхідних даних
        if any(v is None for v in [
            subscription_age, bill_avg, remaining_contract,
            download_avg, upload_avg, service_failure_count,
            is_tv, is_movie, over_limit
        ]):
            return "Будь ласка, заповніть усі поля", px.line(
                title="Історія прогнозів (немає даних)"
            )

        try:
            # Завантаження моделі
            model = load("models/model_RandomForest.joblib")

            # Підготовка вхідних даних
            input_data = prepare_input_data(
                subscription_age, bill_avg, remaining_contract,
                download_avg, upload_avg, service_failure_count,
                is_tv, is_movie, over_limit
            )

            # Виконання прогнозу
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1] * 100

            # Додавання прогнозу до історії
            all_predictions.append({
                "risk_level": prediction,
                "probability": probability,
            })

            # Формування тексту для деталей прогнозу
            prediction_text = html.Div([
                html.H5("Результат прогнозу:"),
                html.P(f"Рівень ризику: {'Високий' if prediction == 1 else 'Низький'}"),
                html.P(f"Ймовірність відтоку: {probability:.2f}%")
            ])

            # Побудова графіка історії прогнозів
            history_df = pd.DataFrame(all_predictions)
            fig = px.line(
                history_df,
                x=history_df.index + 1,  # Номер ітерації
                y="probability",
                markers=True,
                title="Історія прогнозів"
            )
            fig.update_layout(
                xaxis_title="Ітерація",
                yaxis_title="Ймовірність відтоку (%)",
                template="plotly_white"
            )

            return prediction_text, fig

        except Exception as e:
            # У разі помилки
            error_text = html.Div(f"Помилка при обробці даних: {str(e)}", style={"color": "red"})
            empty_fig = px.line(title="Історія прогнозів (немає даних)")
            return error_text, empty_fig
