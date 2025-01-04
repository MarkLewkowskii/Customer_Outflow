from dash import dcc, html

def create_layout():
    return html.Div([
        # Шапка
        html.Nav(className="navbar navbar-expand-lg navbar-dark bg-primary", children=[
            html.Div(className="container-fluid", children=[
                html.A("Проєктна команда 2", className="navbar-brand", href="#"),
                html.Div(className="collapse navbar-collapse", children=[
                    html.Ul(className="navbar-nav ms-auto", children=[
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
        html.Div(className="container-fluid py-4", children=[
            html.Div(className="row", children=[
                # Ліва колонка (35%)
                html.Div(className="col-lg-4", children=[
                    html.Div(className="card shadow-sm", children=[
                        html.Div(className="card-header bg-primary text-white", children="Дані клієнта"),
                        html.Div(className="card-body", children=[
                            html.Div(className="mb-3", children=[
                                html.Label("Тривалість підписки (міс.)", className="form-label"),
                                dcc.Input(id="subscription-age", type="number", placeholder="Введіть кількість місяців", className="form-control")
                            ]),
                            html.Div(className="mb-3", children=[
                                html.Label("Середній рахунок (грн)", className="form-label"),
                                dcc.Input(id="bill-avg", type="number", placeholder="Введіть суму в грн", className="form-control")
                            ]),
                            html.Div(className="mb-3", children=[
                                html.Label("Залишок контракту (міс.)", className="form-label"),
                                dcc.Input(id="remaining-contract", type="number", placeholder="Введіть кількість місяців", className="form-control")
                            ]),
                            html.Div(className="mb-3", children=[
                                html.Label("Середнє завантаження (GB)", className="form-label"),
                                dcc.Input(id="download-avg", type="number", placeholder="Введіть об'єм у GB", className="form-control")
                            ]),
                            html.Div(className="mb-3", children=[
                                html.Label("Середнє вивантаження (GB)", className="form-label"),
                                dcc.Input(id="upload-avg", type="number", placeholder="Введіть об'єм у GB", className="form-control")
                            ]),
                            html.Div(className="mb-3", children=[
                                html.Label("Кількість збоїв сервісу", className="form-label"),
                                dcc.Input(id="service-failure-count", type="number", placeholder="Введіть кількість збоїв", className="form-control")
                            ]),
                            html.Div(className="mb-3", children=[
                                html.Label("Підписка на ТБ", className="form-label"),
                                dcc.Dropdown(id="is-tv-subscriber", options=[
                                    {"label": "Так", "value": 1},
                                    {"label": "Ні", "value": 0}
                                ], placeholder="Оберіть опцію", className="form-select")
                            ]),
                            html.Div(className="mb-3", children=[
                                html.Label("Пакет фільмів", className="form-label"),
                                dcc.Dropdown(id="is-movie-package", options=[
                                    {"label": "Так", "value": 1},
                                    {"label": "Ні", "value": 0}
                                ], placeholder="Оберіть опцію", className="form-select")
                            ]),
                            html.Div(className="mb-3", children=[
                                html.Label("Перевищення ліміту завантаження", className="form-label"),
                                dcc.Dropdown(id="download-over-limit", options=[
                                    {"label": "Так", "value": 1},
                                    {"label": "Ні", "value": 0}
                                ], placeholder="Оберіть опцію", className="form-select")
                            ]),
                            html.Div(className="d-grid gap-2", children=[
                                html.Button("Зробити прогноз", id="predict-button", className="btn btn-primary"),
                                html.Button("Випадкові дані", id="random-button", className="btn btn-secondary")
                            ])
                        ])
                    ])
                ]),

                # Права колонка (65%)
                html.Div(className="col-lg-8", children=[

                ]),


        # Footer
        html.Footer(id="footer", className="bg-dark text-white py-4 mt-4", children=[
            html.Div(className="container", children=[
                html.Div(className="row", children=[
                    html.Div(className="col-md-8", children=[
                        html.H5("Автори", className="text-uppercase fw-bold"),
                        html.Ul(className="list-unstyled", children=[
                            html.Li("Марина Дудик - Team Lead."),
                            html.Li("Георгій Каплицький - Scrum-master."),
                            html.Li("Гліб - Аналітик даних."),
                            html.Li("Ліана Лотарець - Data Scientist."),
                            html.Li("Інна Богуцька - Backend Developer.")
                        ])
                    ]),
                    html.Div(className="col-md-4 text-md-end", children=[
                        html.P("© 2024 Система прогнозування відтоку клієнтів."),
                        html.P("Всі права захищено.")
                    ])
                ])
            ])
        ])
    ])
