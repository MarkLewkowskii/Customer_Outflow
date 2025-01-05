from dash import Dash
from app_layout import app_layout
from src.callbacks import register_callbacks

# Ініціалізація додатку
app = Dash(__name__, external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"])

# Додавання макету
app.layout = app_layout

# Реєстрація зворотних викликів
register_callbacks(app)

# Запуск додатку
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
