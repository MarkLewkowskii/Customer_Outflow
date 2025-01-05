import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
from faker_new_client import generate_fake_client_data
from model_training import predict

# Підключення Bootstrap через CDN
app = Dash(__name__, external_stylesheets=[
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
])

# Глобальні змінні для збереження всіх прогнозів
all_predictions = []

# Макет програми
app.layout = html.Div([
    # Header
    html.Nav(className="navbar navbar-expand-lg navbar-dark bg-primary", children=[
        html.Div(className="container-fluid", children=[
            html.A("Project team 2", className="navbar-brand", href="#"),
            html.Button(className="navbar-toggler", type="button", **{
                "data-bs-toggle": "collapse",
                "data-bs-target": "#navbarNav",
                "aria-controls": "navbarNav",
                "aria-expanded": "false",
                "aria-label": "Toggle navigation"
            }, children=[
                html.Span(className="navbar-toggler-icon")
            ]),
            html.Div(className="collapse navbar-collapse", id="navbarNav", children=[
                html.Ul(className="navbar-nav", children=[
                    html.Li(className="nav-item", children=[
                        html.A("Головна", className="nav-link active", href="#")
                    ]),
                    html.Li(className="nav-item", children=[
                        html.A("Про нас", className="nav-link", href="#footer")
                    ])
                ])
            ])
        ])
    ]),

    # Основний контент
    html.Div(className="container py-5", children=[
        html.Div(className="text-center mb-4", children=[
            html.H1("Система прогнозування відтоку клієнтів", className="display-4 text-primary"),
            html.P("Заповніть дані клієнта, щоб дізнатися прогноз", className="lead")
        ]),

        html.Div(className="row", children=[
        # Ліва колонка: форма введення
        html.Div(className="col-md-6 mb-4", children=[
            html.Div(className="card shadow-sm", children=[
                html.Div(className="card-header text-white bg-primary", children="Дані клієнта"),
                html.Div(className="card-body", children=[
                    html.Div(className="mb-3", children=[
                        html.Label("Тривалість підписки (міс.)", className="form-label"),
                        dcc.Input(
                            id="subscription-age",
                            type="number",
                            placeholder="Введіть кількість місяців",
                            className="form-control"
                        )
                    ]),
                    html.Div(className="mb-3", children=[
                        html.Label("Середній рахунок (грн)", className="form-label"),
                        dcc.Input(
                            id="bill-avg",
                            type="number",
                            placeholder="Введіть суму в грн",
                            className="form-control"
                        )
                    ]),
                    html.Div(className="mb-3", children=[
                        html.Label("Залишок контракту (міс.)", className="form-label"),
                        dcc.Input(
                            id="remaining-contract",
                            type="number",
                            placeholder="Введіть кількість місяців",
                            className="form-control"
                        )
                    ]),
                    html.Div(className="mb-3", children=[
                        html.Label("Середнє завантаження (GB)", className="form-label"),
                        dcc.Input(
                            id="download-avg",
                            type="number",
                            placeholder="Введіть об'єм у GB",
                            className="form-control"
                        )
                    ]),
                    html.Div(className="mb-3", children=[
                        html.Label("Середнє вивантаження (GB)", className="form-label"),
                        dcc.Input(
                            id="upload-avg",
                            type="number",
                            placeholder="Введіть об'єм у GB",
                            className="form-control"
                        )
                    ]),
                    html.Div(className="mb-3", children=[
                        html.Label("Кількість збоїв сервісу", className="form-label"),
                        dcc.Input(
                            id="service-failure-count",
                            type="number",
                            placeholder="Введіть кількість збоїв",
                            className="form-control"
                        )
                    ]),
                    html.Div(className="mb-3", children=[
                        html.Label("Підписка на ТБ", className="form-label"),
                        dcc.Dropdown(
                            id="is-tv-subscriber",
                            options=[
                                {"label": "Так", "value": 1},
                                {"label": "Ні", "value": 0}
                            ],
                            placeholder="Оберіть опцію",
                            className="form-select"
                        )
                    ]),
                    html.Div(className="mb-3", children=[
                        html.Label("Пакет фільмів", className="form-label"),
                        dcc.Dropdown(
                            id="is-movie-package",
                            options=[
                                {"label": "Так", "value": 1},
                                {"label": "Ні", "value": 0}
                            ],
                            placeholder="Оберіть опцію",
                            className="form-select"
                        )
                    ]),
                    html.Div(className="mb-3", children=[
                        html.Label("Перевищення ліміту завантаження", className="form-label"),
                        dcc.Dropdown(
                            id="download-over-limit",
                            options=[
                                {"label": "Так", "value": 1},
                                {"label": "Ні", "value": 0}
                            ],
                            placeholder="Оберіть опцію",
                            className="form-select"
                        )
                    ]),
                    html.Div(className="d-grid gap-2", children=[
                        html.Button(
                            "Зробити прогноз",
                            id="predict-button",
                            className="btn btn-primary"
                        ),
                        html.Button(
                            "Випадкові дані",
                            id="random-button",
                            className="btn btn-secondary"
                        )
                    ])
                ])
            ])
        ]),

        # Права колонка: результати
        html.Div(className="col-md-6", children=[
            html.Div(className="card shadow-sm", children=[
                html.Div(className="card-header text-white bg-success", children="Результати прогнозу"),
                html.Div(className="card-body", children=[
                    html.Div(id="prediction-output", className="alert alert-primary"),
                    html.Div(id="prediction-details", className="alert alert-secondary mt-3")
                ])
            ]),
            # Графік
            html.Div(className="mt-4", children=[
                html.Div(className="card shadow-sm", children=[
                    html.Div(className="card-header text-white bg-info", children="Історія прогнозів"),
                    html.Div(className="card-body", children=[
                        dcc.Graph(id="history-graph")
                    ])
                ])
            ])
        ])
    ])
]),

    # Footer
    html.Footer(id="footer", className="bg-dark text-white py-4 mt-4", children=[
        html.Div(className="container", children=[
            html.Div(className="row", children=[
                # Перша колонка: автори
                html.Div(className="col-md-8", children=[
                    html.H5("Автори", className="text-uppercase fw-bold"),
                    html.Ul(className="list-unstyled", children=[
                        html.Li("Maryna Dudik - Team Lead: Організація роботи, документація."),
                        html.Li("Heorhii Kaplytskyi - Scrum-master: Організація роботи, документація."),
                        html.Li("Gleb - Data Analyst: Аналіз даних."),
                        html.Li("Gleb - Data Engineer: Підготовка даних."),
                        html.Li("Liana Lotarets - Data Scientist: Навчання моделей."),
                        html.Li("Inna Bogutska - Backend Developer: Реалізація інтерфейсу."),
                        html.Li("Maryna Dudik - DevOps-інженер: Контейнеризація.")
                    ])
                ]),
                # Друга колонка: права
                html.Div(className="col-md-4 text-md-end", children=[
                    html.P("© 2024 Система прогнозування відтоку клієнтів."),
                    html.P("Всі права захищено.")
                ])
            ])
        ])
    ])
])

# Callback для генерації випадкових даних
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
        return [None] * 9  # Початкове значення
    fake_data = generate_fake_client_data()
    return [
        fake_data["subscription_age"],
        fake_data["bill_avg"],
        fake_data["reamining_contract"],
        fake_data["download_avg"],
        fake_data["upload_avg"],
        fake_data["service_failure_count"],
        fake_data["is_tv_subscriber"],
        fake_data["is_movie_package_subscriber"],
        fake_data["download_over_limit"]
    ]

# Callback для прогнозу
@app.callback(
    [Output("prediction-output", "children"),
     Output("prediction-details", "children"),
     Output("history-graph", "figure")],
    [Input("predict-button", "n_clicks")],
    [State("subscription-age", "value"),
     State("bill-avg", "value"),
     State("remaining-contract", "value"),
     State("download-avg", "value"),
     State("upload-avg", "value"),
     State("service-failure-count", "value"),
     State("is-tv-subscriber", "value"),
     State("is-movie-package", "value"),
     State("download-over-limit", "value")]
)

def make_prediction(n_clicks, subscription_age, bill_avg, remaining_contract,
                    download_avg, upload_avg, service_failure_count,
                    is_tv, is_movie, over_limit):
    global all_predictions

    if n_clicks is None:
        return "Введіть дані та натисніть кнопку для прогнозування", "", px.line(title="Історія прогнозів")

    # Перевірка наявності всіх необхідних даних
    if any(v is None for v in [subscription_age, bill_avg, remaining_contract,
                               download_avg, upload_avg, service_failure_count,
                               is_tv, is_movie, over_limit]):
        return "Будь ласка, заповніть усі поля", "", px.line(title="Історія прогнозів")

    try:
        # Створення DataFrame з введених даних
        input_data = pd.DataFrame({
            'is_tv_subscriber': [int(is_tv)],
            'is_movie_package_subscriber': [int(is_movie)],
            'subscription_age': [float(subscription_age)],
            'bill_avg': [float(bill_avg)],
            'reamining_contract': [float(remaining_contract)],
            'service_failure_count': [int(service_failure_count)],
            'download_avg': [float(download_avg)],
            'upload_avg': [float(upload_avg)],
            'download_over_limit': [int(over_limit)]
        })

        # Використання функції predict для отримання прогнозу
        prediction_result = predict(input_data)

        # Отримання результатів
        prediction_value = prediction_result['prediction'][0]
        probability = prediction_result['probability_of_churn'][0]

        all_predictions.append({
            "Ймовірність відтоку (%)": probability,
            "Прогноз": "Високий ризик" if prediction_value == 1 else "Низький ризик",
            "Ітерація": len(all_predictions) + 1
        })

        prediction_text = html.Div([
            html.H3(f"{'Високий' if prediction_value == 1 else 'Низький'} ризик відтоку", style={'color': 'red' if prediction_value == 1 else 'green'}),
            html.P(f"Ймовірність відтоку клієнта: {probability:.2f}%"),
        ])

        details = html.Div([
            html.H5("Введені дані:"),
            html.Ul([
                html.Li(f"Тривалість підписки: {subscription_age} місяців"),
                html.Li(f"Середній рахунок: {bill_avg} грн"),
                html.Li(f"Залишок контракту: {remaining_contract} місяців"),
                html.Li(f"Середнє завантаження: {download_avg} GB"),
                html.Li(f"Середнє вивантаження: {upload_avg} GB"),
                html.Li(f"Кількість збоїв сервісу: {service_failure_count}"),
                html.Li("Наявність ТБ підписки: " + ("Так" if is_tv else "Ні")),
                html.Li("Наявність пакету фільмів: " + ("Так" if is_movie else "Ні")),
                html.Li("Перевищення ліміту завантаження: " + ("Так" if over_limit else "Ні")),
            ])
        ])

        # Побудова графіка історії прогнозів
        history_df = pd.DataFrame(all_predictions)
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

        return prediction_text, details, fig

    except Exception as e:
        return html.Div(f"Помилка при обробці даних: {str(e)}", style={"color": "red"}), "", px.line(title="Історія прогнозів")


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
