import plotly.express as px
import pandas as pd
import json
import os
from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
from faker_new_client import generate_fake_client_data
from joblib import load

# Ініціалізація Dash-додатку
app = Dash(__name__, external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"])

all_predictions = []

# Макет додатку
app.layout = html.Div(className='d-flex flex-column h-100', children=[
    # Header/NavBar
    html.Nav(className='py-2 bg-light border-bottom', children=[
        html.Div(className='container d-flex flex-wrap', children=[
            html.Ul(className='nav me-auto', children=[
                html.Li(className="nav-item", children=[
                    html.A(className="nav-link active", href="#", children="Home")
                ]),
                html.Li(className="nav-item", children=[
                    html.A(className="nav-link", href="#footer", children="Contributors")
                ])
            ]),
            html.Ul(className='nav', children=[
                html.Li(className="nav-item", children=[
                    html.A(className="nav-link active", href="#", children="Sign up")
                ]),
                html.Li(className="nav-item", children=[
                    html.A(className="nav-link", href="#footer", children="Login")
                ])
            ])
        ])
    ]),
    html.Header(className="py-3 mb-4 border-bottom", children=[
        html.Div(
            className="container d-flex flex-wrap justify-content-center", children=[
                html.A(className="d-flex align-items-center mb-3 mb-lg-0 me-lg-auto text-dark text-decoration-none",
                       href="/", children=[
                html.Img(src="assets/images/brand/logo/ProjectTeamUI_logo.svg", className="me-2", style={"height": "40px"}),
                # Шлях до логотипу та стиль
                html.Span(className='fs-4', children=["Project Team 2"])
            ]),
                html.Form(className="col-12 col-lg-auto mb-3 mb-lg-0", children=[
                    dcc.Input(className="form-control", type="search", placeholder="Search", id='search-input')
                ])
            ])
    ]),
    # Main Content Placeholder
    html.Main(className='container-fluid', children=[
        html.Div(className='row', children=[
            html.Div(className='col-md-2 d-md-block bg-light sidebar collapse', children=[
                html.Div(className='col- col-lg-auto mb-lg-15 mt-3 mx-4', children=[
                    html.Div(className="card-header text-white bg-primary rounded-pill py-3 px-4 fs-4", children="Дані клієнта"),
                    html.Div(className="card-body", children=[
                        html.Div(className="mb-1", children=[
                            html.Label("Тривалість підписки (міс.)", className="form-label"),
                            dcc.Input(
                                id="subscription-age",
                                type="number",
                                placeholder="Введіть кількість місяців",
                                className="form-control"
                            )
                        ]),
                        html.Div(className="mb-1", children=[
                            html.Label("Середній рахунок (грн)", className="form-label"),
                            dcc.Input(
                                id="bill-avg",
                                type="number",
                                placeholder="Введіть суму в грн",
                                className="form-control"
                            )
                        ]),
                        html.Div(className="mb-1", children=[
                            html.Label("Залишок контракту (міс.)", className="form-label"),
                            dcc.Input(
                                id="remaining-contract",
                                type="number",
                                placeholder="Введіть кількість місяців",
                                className="form-control"
                            )
                        ]),
                        html.Div(className="mb-1", children=[
                            html.Label("Середнє завантаження (GB)", className="form-label"),
                            dcc.Input(
                                id="download-avg",
                                type="number",
                                placeholder="Введіть об'єм у GB",
                                className="form-control"
                            )
                        ]),
                        html.Div(className="mb-1", children=[
                            html.Label("Середнє вивантаження (GB)", className="form-label"),
                            dcc.Input(
                                id="upload-avg",
                                type="number",
                                placeholder="Введіть об'єм у GB",
                                className="form-control"
                            )
                        ]),
                        html.Div(className="mb-1", children=[
                            html.Label("Кількість збоїв сервісу", className="form-label"),
                            dcc.Input(
                                id="service-failure-count",
                                type="number",
                                placeholder="Введіть кількість збоїв",
                                className="form-control"
                            )
                        ]),
                        html.Div(className="mb-1", children=[
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
                        html.Div(className="mb-1", children=[
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
                        html.Div(className="mb-1", children=[
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

            html.Div(className='col-md-9', children=[
                # Блок з картками
                html.Div(className='row', children=[
                    # Перша картка
                    html.Div(className='col-xl-3 col-lg-6 col-md-12 mb-4', children=[
                        html.Div(className='card h-100', children=[
                            html.Div(className='card-body', children=[
                                html.Div(className='d-flex justify-content-between align-items-center mb-3', children=[
                                    html.H4('Ризик відтоку', className='mb-0'),
                                    html.Div(className='icon-shape icon-md bg-primary text-white rounded-circle',
                                             children=[
                                                 html.I(className='feather feather-briefcase')
                                             ])
                                ]),
                                html.Div(className='lh-1', children=[
                                    html.H1(id="risk-output", className='mb-1 fw-bold'),
                                ])
                            ])
                        ])
                    ]),
                    # Друга картка
                    html.Div(className='col-xl-3 col-lg-6 col-md-12 mb-4', children=[
                        html.Div(className='card h-100', children=[
                            html.Div(className='card-body', children=[
                                html.Div(className='d-flex justify-content-between align-items-center mb-3', children=[
                                    html.H4('Ймовірність відтоку', className='mb-0'),
                                    html.Div(className='icon-shape icon-md bg-success text-white rounded-circle',
                                             children=[
                                                 html.I(className='feather feather-list')
                                             ])
                                ]),
                                html.Div(className='lh-1', children=[
                                    html.H1(id="churn-probability-output", className='mb-1 fw-bold'),
                                ])
                            ])
                        ])
                    ]),
                    # Третя картка
                    html.Div(className='col-xl-3 col-lg-6 col-md-12 mb-4', children=[
                        html.Div(className='card h-100', children=[
                            html.Div(className='card-body', children=[
                                html.Div(className='d-flex justify-content-between align-items-center mb-3', children=[
                                    html.H4('Кількість прогнозів', className='mb-0'),
                                    html.Div(className='icon-shape icon-md bg-warning text-white rounded-circle',
                                             children=[
                                                 html.I(className='feather feather-users')
                                             ])
                                ]),
                                html.Div(className='lh-1', children=[
                                    html.H1(id="total-predictions-output", className='mb-1 fw-bold'),
                                ])
                            ])
                        ])
                    ]),
                    # Четверта картка
                    html.Div(className='col-xl-3 col-lg-6 col-md-12 mb-4', children=[
                        html.Div(className='card h-100', children=[
                            html.Div(className='card-body', children=[
                                html.Div(className='d-flex justify-content-between align-items-center mb-3', children=[
                                    html.H4('Середня ймовірність відтоку', className='mb-0'),
                                    html.Div(className='icon-shape icon-md bg-danger text-white rounded-circle',
                                             children=[
                                                 html.I(className='feather feather-target')
                                             ])
                                ]),
                                html.Div(className='lh-1', children=[
                                    html.H1(id="average-churn-output", className='mb-1 fw-bold'),
                                ])
                            ])
                        ])
                    ]),
                ]),
                html.Div(className='row', children=[
                    # Table Block (Active Projects)
                    html.Div(className='col mb-5', children=[
                        html.Div(className='card', children=[
                            html.Div(className='card-header', children=[
                                html.H4("Введені дані", className='mb-0')
                            ]),
                            html.Div(className='card-body', children=[
                                html.Div(className='table-responsive table-card', children=[
                                    html.Table(className='table text-nowrap mb-0 table-centered table-hover', children=[
                                        html.Thead(className='table-light', children=[
                                            html.Tr([
                                                html.Th("Параметр"),
                                                html.Th("Значення")
                                            ])
                                        ]),
                                        html.Tbody(id="input-data-table", children=[
                                            html.Tr([html.Td("Тривалість підписки"), html.Td(id="input-subscription-age")]),
                                            html.Tr([html.Td("Середній рахунок"), html.Td(id="input-bill-avg")]),
                                            html.Tr([html.Td("Залишок контракту"), html.Td(id="input-remaining-contract")]),
                                            html.Tr([html.Td("Середнє завантаження"), html.Td(id="input-download-avg")]),
                                            html.Tr([html.Td("Середнє вивантаження"), html.Td(id="input-upload-avg")]),
                                            html.Tr([html.Td("Кількість збоїв сервісу"), html.Td(id="input-service-failure-count")]),
                                            html.Tr([html.Td("Наявність ТБ підписки"), html.Td(id="input-tv-subscriber")]),
                                            html.Tr([html.Td("Наявність пакету фільмів"), html.Td(id="input-movie-package")]),
                                            html.Tr([html.Td("Перевищення ліміту завантаження"), html.Td(id="input-over-limit")]),
                                        ])
                                    ])
                                ])
                            ])
                        ])
                    ]),
                    # Circular Graph Block (Tasks Performance)
                    html.Div(className='col mb-5', children=[
                        html.Div(className='card', children=[
                            html.Div(className='card-header d-flex align-items-center justify-content-between',
                                     children=[
                                         html.Div([
                                             html.H4("Порівняння моделей", className='mb-0')
                                         ])
                                     ]),
                            html.Div(className='card-body', children=[
                                dcc.Graph(
                                    id="model-comparison-chart",
                                    config={"displayModeBar": False},
                                    style={"height": "475px"}
                                )
                            ])
                        ])
                    ])
                ]),
                # Графік історії прогнозів
                html.Div(className='row', children=[
                    html.Div(className='card', children=[
                        html.Div(className='card-header', children=[
                            html.H4("Історія прогнозів", className='mb-0')
                        ]),
                        html.Div(className='card-body', children=[
                            dcc.Graph(id="history-graph")
                        ])
                    ])
                ])
            ])
        ])
    ]),

    # Footer
    html.Footer(className="footer mt-8 py-3 bg-light", children=[
        html.Div(id='footer', className="container", children=[
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
        ])
    ])
])


# Callbacks
# @app.callback(
#     Output("search-results", "children"),
#     Input("search-input", "value")
# )
# def update_search_results(search_value):
#     if search_value:
#         return f"Search results for: {search_value}"
#     return "No search query entered."


# Callback для генерації випадкових даних
# Callback for generating random data
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

# Callback для прогнозу
@app.callback(
    Input("predict-button", "n_clicks"),
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
    ],
)
def make_prediction(n_clicks, subscription_age, bill_avg, remaining_contract,
                    download_avg, upload_avg, service_failure_count,
                    is_tv, is_movie, over_limit):
    global all_predictions

    # Перевірка: якщо кнопку не натискали
    if n_clicks is None:
        return

    # Перевірка: всі поля повинні бути заповнені
    if any(v is None for v in [subscription_age, bill_avg, remaining_contract,
                               download_avg, upload_avg, service_failure_count,
                               is_tv, is_movie, over_limit]):
        return

    try:
        # Завантаження моделі
        model_path = "models/model_RandomForest.joblib"
        model = load(model_path)

        # Формування даних для прогнозу
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

        # Отримання прогнозу
        prediction_value = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1] * 100

        # Додавання тільки ймовірностей до all_predictions
        all_predictions.append(probability)

    except Exception as e:
        print(f"Помилка при обробці даних: {e}")


@app.callback(
    [Output("risk-output", "children"),
     Output("churn-probability-output", "children"),
     Output("total-predictions-output", "children"),
     Output("average-churn-output", "children")],
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
def update_cards(n_clicks, subscription_age, bill_avg, remaining_contract,
                 download_avg, upload_avg, service_failure_count,
                 is_tv, is_movie, over_limit):
    global all_predictions

    if n_clicks is None:
        return "N/A", "N/A", "0", "0%"

    # Validate inputs
    if any(v is None for v in [subscription_age, bill_avg, remaining_contract,
                               download_avg, upload_avg, service_failure_count,
                               is_tv, is_movie, over_limit]):
        return "Incomplete Data", "Incomplete Data", "0", "0%"

    try:
        # Load model
        model_path = 'models/model_RandomForest.joblib'
        model = load(model_path)

        # Create DataFrame with input data
        input_data = pd.DataFrame({
            'is_tv_subscriber': [int(is_tv)],
            'is_movie_package_subscriber': [int(is_movie)],
            'subscription_age': [float(subscription_age)],
            'bill_avg': [float(bill_avg)],
            'remaining_contract': [float(remaining_contract)],
            'service_failure_count': [int(service_failure_count)],
            'download_avg': [float(download_avg)],
            'upload_avg': [float(upload_avg)],
            'download_over_limit': [int(over_limit)]
        })

        # Get prediction
        prediction_value = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1] * 100

        # Calculate average churn probability
        average_churn = sum(all_predictions) / len(all_predictions) if all_predictions else 0

        return (
            "Високий ризик" if prediction_value == 1 else "Низький ризик",
            f"{probability:.2f}%",
            str(len(all_predictions)),
            f"{average_churn:.2f}%"
        )

    except Exception as e:
        return f"Error: {str(e)}", "Error", "0", "0%"

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
    # Завантаження даних з JSON
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '../results/model_evaluation.json')

    with open(file_path) as f:
        model_data = json.load(f)

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
        classification_report = metrics["classification_report"]
        # Використовуємо абревіатуру моделі
        abbreviated_name = abbreviations.get(model_name, model_name)
        data.append({
            "Model": abbreviated_name,
            "Metric": "Accuracy",
            "Value": classification_report["accuracy"]
        })
        data.append({
            "Model": abbreviated_name,
            "Metric": "Model Size (MB)",
            "Value": metrics["model_size_mb"]
        })
        data.append({
            "Model": abbreviated_name,
            "Metric": "Precision",
            "Value": classification_report["macro avg"]["precision"]
        })
        data.append({
            "Model": abbreviated_name,
            "Metric": "Recall",
            "Value": classification_report["macro avg"]["recall"]
        })

    df = pd.DataFrame(data)

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
    fig.update_traces(text=df["Value"].round(3), textposition='outside')

    # Покращення дизайну
    fig.update_layout(
        title_font=dict(size=20, family='Arial'),
        xaxis_title="Models",
        yaxis_title="Metric Value",
        legend_title="Metrics",
        xaxis_tickangle=-45,
        bargap=0.15  # Відстань між групами барів
    )

    # Показати графік
    return fig

# графік історії прогнозу
@app.callback(
    Output("history-graph", "figure"),
    Input("predict-button", "n_clicks")
)
def update_history_graph(n_clicks):
    if not all_predictions:
        # Повертаємо порожній графік, якщо немає прогнозів
        return px.line(title="Історія прогнозів")

    # Побудова графіка на основі історії прогнозів
    history_df = pd.DataFrame({
        "Ітерація": list(range(1, len(all_predictions) + 1)),
        "Ймовірність відтоку (%)": all_predictions
    })

    fig = px.line(
        history_df,
        x="Ітерація",
        y="Ймовірність відтоку (%)",
        markers=True,
        title="Історія прогнозів",
    )

    # Налаштування осей та стилю
    fig.update_layout(
        xaxis_title="Ітерація",
        yaxis_title="Ймовірність відтоку (%)",
        template="plotly_white",
        xaxis=dict(tickmode="linear"),  # Показувати всі ітерації
    )

    return fig

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)