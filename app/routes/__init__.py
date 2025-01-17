# myPortfolio/app/routes/__init__.py
from routes import home_page


def register_routes(app):
    app.register_blueprint(home_page)
