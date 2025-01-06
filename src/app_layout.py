from dash import dcc, html

def app_layout():
    return html.Div(className='d-flex flex-column h-100', children=[
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
                html.Div(className='card-body', children=[
                    html.H2(className="card-title", children="Дані клієнта"),
                    html.Div(className="card-body", children=[
                        html.Div(className="mb-1", children=[
                            html.Label("Оберіть модель для прогнозу", className="form-label"),
                            dcc.Dropdown(
                                id="model-selector",
                                options=[
                                    {"label": "Random Forest", "value": "RandomForest"},
                                    {"label": "Gradient Boosting", "value": "GradientBoosting"},
                                    {"label": "Hist Gradient Boosting", "value": "HistGradientBoosting"},
                                    {"label": "Logistic Regression", "value": "LogisticRegression"}
                                ],
                                value="RandomForest",  # Default selection
                                placeholder="Оберіть модель",
                                className="form-select"
                            )
                        ]),

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
                            html.Label("Середній рахунок (грн.)", className="form-label"),
                            dcc.Input(
                                id="bill-avg",
                                type="number",
                                placeholder="Введіть середній рахунок",
                                className="form-control"
                            )
                        ]),
                        html.Div(className="mb-1", children=[
                            html.Label("Тривалість контракту (міс.)", className="form-label"),
                            dcc.Input(
                                id="reamining_contract",
                                type="number",
                                placeholder="Введіть тривалість контракту",
                                className="form-control"
                            )
                        ]),
                        html.Div(className="mb-1", children=[
                            html.Label("Середнє завантаження (ГБ)", className="form-label"),
                            dcc.Input(
                                id="download-avg",
                                type="number",
                                placeholder="Введіть середнє завантаження",
                                className="form-control"
                            )
                        ]),
                        html.Div(className="mb-1", children=[
                            html.Label("Середнє вивантаження (ГБ)", className="form-label"),
                            dcc.Input(
                                id="upload-avg",
                                type="number",
                                placeholder="Введіть середнє вивантаження",
                                className="form-control"
                            )
                        ]),
                        html.Div(className="mb-1", children=[
                            html.Label("Кількість збоїв сервісу", className="form-label"),
                            dcc.Input(
                                id="service-failure-count",
                                type="number",
                                placeholder="Введіть кількість збоїв сервісу",
                                className="form-control"
                            )
                        ]),
                        html.Div(className="mb-1", children=[
                            html.Label("Чи є підписка на ТВ", className="form-label"),
                            dcc.Input(
                                id="is-tv-subscriber",
                                type="number",
                                placeholder="Введіть 1 якщо є, 0 якщо немає",
                                className="form-control"
                            )
                        ]),
                        html.Div(className="mb-1", children=[
                            html.Label("Чи є підписка на кіно", className="form-label"),
                            dcc.Input(
                                id="is-movie-package",
                                type="number",
                                placeholder="Введіть 1 якщо є, 0 якщо немає",
                                className="form-control"
                            )
                        ]),
                        html.Div(className="mb-1", children=[
                            html.Label("Завантаження понад ліміт", className="form-label"),
                            dcc.Input(
                                id="download-over-limit",
                                type="number",
                                placeholder="Введіть 1 якщо є, 0 якщо немає",
                                className="form-control"
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
                                    html.H1(id="risk-output", className='mb-1 fw-bold', style={"color": "#000"}),
                                    # Початковий колір чорний
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
                                            html.Tr(
                                                [html.Td("Тривалість підписки"), html.Td(id="input-subscription-age")]),
                                            html.Tr([html.Td("Середній рахунок"), html.Td(id="input-bill-avg")]),
                                            html.Tr(
                                                [html.Td("Залишок контракту"), html.Td(id="input-reamining_contract")]),
                                            html.Tr(
                                                [html.Td("Середнє завантаження"), html.Td(id="input-download-avg")]),
                                            html.Tr([html.Td("Середнє вивантаження"), html.Td(id="input-upload-avg")]),
                                            html.Tr([html.Td("Кількість збоїв сервісу"),
                                                     html.Td(id="input-service-failure-count")]),
                                            html.Tr(
                                                [html.Td("Наявність ТБ підписки"), html.Td(id="input-tv-subscriber")]),
                                            html.Tr([html.Td("Наявність пакету фільмів"),
                                                     html.Td(id="input-movie-package")]),
                                            html.Tr([html.Td("Перевищення ліміту завантаження"),
                                                     html.Td(id="input-over-limit")]),
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
