from dash import Dash, dcc, html, Input, Output, State
import pandas as pd
from model_training import predict

app = Dash(__name__)

# Стилі
CARD_STYLE = {
    'padding': '20px',
    'margin': '10px',
    'borderRadius': '5px',
    'boxShadow': '0 4px 6px 0 rgba(0, 0, 0, 0.1)',
    'backgroundColor': 'white'
}

INPUT_STYLE = {
    'width': '100%',
    'marginBottom': '10px',
    'padding': '8px',
    'borderRadius': '4px',
    'border': '1px solid #ddd'
}

BUTTON_STYLE = {
    'width': '100%',
    'padding': '10px',
    'backgroundColor': '#007bff',
    'color': 'white',
    'border': 'none',
    'borderRadius': '4px',
    'cursor': 'pointer'
}

# Layout 
app.layout = html.Div([
    html.H1("Система прогнозування відтоку клієнтів", 
            style={'textAlign': 'center', 'margin': '20px'}),
    
    html.Div([
        # Ліва колонка - введення даних
        html.Div([
            html.Div(style=CARD_STYLE, children=[
                html.H4("Дані клієнта"),
                
                # Числові входи
                html.H5("Числові параметри", style={'marginTop': '20px'}),
                html.Div([
                    html.Label("Тривалість підписки (міс.)"),
                    dcc.Input(
                        id="subscription-age",
                        type="number",
                        min=0,
                        style=INPUT_STYLE,
                        placeholder="Введіть кількість місяців"
                    ),
                    
                    html.Label("Середній рахунок"),
                    dcc.Input(
                        id="bill-avg",
                        type="number",
                        min=0,
                        style=INPUT_STYLE,
                        placeholder="Введіть суму в грн"
                    ),
                    
                    html.Label("Залишок контракту (міс.)"),
                    dcc.Input(
                        id="remaining-contract",
                        type="number",
                        min=0,
                        style=INPUT_STYLE,
                        placeholder="Введіть кількість місяців"
                    ),
                    
                    html.Label("Середнє завантаження (GB)"),
                    dcc.Input(
                        id="download-avg",
                        type="number",
                        min=0,
                        style=INPUT_STYLE,
                        placeholder="Введіть об'єм у GB"
                    ),
                    
                    html.Label("Середнє вивантаження (GB)"),
                    dcc.Input(
                        id="upload-avg",
                        type="number",
                        min=0,
                        style=INPUT_STYLE,
                        placeholder="Введіть об'єм у GB"
                    ),
                    
                    html.Label("Кількість збоїв сервісу"),
                    dcc.Input(
                        id="service-failure-count",
                        type="number",
                        min=0,
                        style=INPUT_STYLE,
                        placeholder="Введіть кількість збоїв"
                    ),
                ]),
                
                # Категоріальні входи
                html.H5("Додаткові параметри", style={'marginTop': '20px'}),
                html.Div([
                    html.Label("Підписка на ТБ"),
                    dcc.Dropdown(
                        id="is-tv-subscriber",
                        options=[
                            {"label": "Так", "value": 1},
                            {"label": "Ні", "value": 0}
                        ],
                        style={'marginBottom': '10px'},
                        placeholder="Оберіть опцію"
                    ),
                    
                    html.Label("Пакет фільмів"),
                    dcc.Dropdown(
                        id="is-movie-package",
                        options=[
                            {"label": "Так", "value": 1},
                            {"label": "Ні", "value": 0}
                        ],
                        style={'marginBottom': '10px'},
                        placeholder="Оберіть опцію"
                    ),
                    
                    html.Label("Перевищення ліміту завантаження"),
                    dcc.Dropdown(
                        id="download-over-limit",
                        options=[
                            {"label": "Так", "value": 1},
                            {"label": "Ні", "value": 0}
                        ],
                        style={'marginBottom': '20px'},
                        placeholder="Оберіть опцію"
                    ),
                ]),
                
                # Кнопка прогнозування
                html.Button(
                    "Зробити прогноз",
                    id="predict-button",
                    style=BUTTON_STYLE
                ),
            ]),
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        # Права колонка - результати
        html.Div([
            html.Div(style=CARD_STYLE, children=[
                html.H4("Результати прогнозування"),
                html.Div(id="prediction-output"),
                html.Div(id="prediction-details"),
            ]),
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '4%'}),
    ])
])

@app.callback(
    [Output("prediction-output", "children"),
     Output("prediction-details", "children")],
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
    if n_clicks is None:
        return "Введіть дані та натисніть кнопку для прогнозування", ""
    
    # Перевірка наявності всіх необхідних даних
    if any(v is None for v in [subscription_age, bill_avg, remaining_contract,
                              download_avg, upload_avg, service_failure_count,
                              is_tv, is_movie, over_limit]):
        return "Будь ласка, заповніть усі поля", ""
    
    try:
        # Створення DataFrame з введених даних у правильному порядку
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
        
        # Отримання прогнозу
        result = predict(input_data)
        prediction_value = result['prediction'].iloc[0]
        
        # Форматування виведення
        risk_level = "Високий" if prediction_value == 1 else "Низький"
        color = "red" if prediction_value == 1 else "green"
        
        prediction_text = html.Div([
            html.H3(f"{risk_level} ризик відтоку", style={'color': color}),
            html.P(
                "Клієнт має високу ймовірність припинення користування послугами."
                if prediction_value == 1 else
                "Клієнт ймовірно продовжить користуватися послугами."
            )
        ])
        
        # Додаткова інформація
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
        
        return prediction_text, details
    
    except Exception as e:
        return f"Помилка при обробці даних: {str(e)}", ""

if __name__ == '__main__':
    app.run_server(debug=True)