# myPortfolio/app/__init__.py
import os
import logging
from flask import Flask, render_template
from flask_session import Session
from logging.handlers import RotatingFileHandler
from datetime import datetime
import pytz

from .extensions import db, migrate, login_manager, csrf
from .routes import register_routes
from .config import DevelopmentConfig, ProductionConfig

def create_app():
    """Создание и настройка экземпляра Flask-приложения"""
    app = Flask(__name__)

    # Добавление глобальной переменной текущей даты для шаблонов
    app.jinja_env.globals['now'] = datetime.now

    # Определение конфигурации по окружению
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Логирование
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=5)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    file_handler.setLevel(app.config['LOG_LEVEL'])
    app.logger.addHandler(file_handler)
    app.logger.setLevel(app.config['LOG_LEVEL'])
    app.logger.info(f"Application started in {env} mode")

    # Обработка ошибки 500
    @app.errorhandler(500)
    def handle_500_error(e):
        app.logger.error(f"Internal Server Error: {e}", exc_info=True)
        return render_template('error/500.html'), 500

    # Инициализация расширений
    csrf.init_app(app)
    Session(app)
    register_routes(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Конфигурация Flask-Login
    login_manager.login_view = 'users.login'
    login_manager.login_message = False

    # Определение функции загрузки пользователя
    from app.models.user import User  # <-- Импортируем из нового файла
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except (ValueError, TypeError):
            return None

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'])
