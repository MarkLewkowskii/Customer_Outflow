from dash import Dash
from app_layout import app_layout
from callbacks import register_callbacks

app = Dash(__name__, external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"])
app.layout = app_layout()
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
