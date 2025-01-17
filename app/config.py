# myPortfolio/app/config.py
import os
from dotenv import load_dotenv
import redis

# Загрузка переменных окружения из файла .env
load_dotenv('.env')

class Config:
    """Базовая конфигурация"""
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = False
    PROPAGATE_EXCEPTIONS = True
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = '/static/upload/'
    SERVER_PATH = os.path.join(ROOT, UPLOAD_PATH)

    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY', 'qwerty12345')

    # Конфигурация для базы данных MySQL
    USER = os.environ.get('MYSQL_USER', 'test')
    PASSWORD = os.environ.get('MYSQL_PASSWORD', 'test')
    HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
    PORT = os.environ.get('MYSQL_PORT', '3306')
    DB = os.environ.get('MYSQL_DB', 'my_portfolio_db')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Секретный ключ для Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'qwerty123456')

    # Конфигурация для сессий
    SESSION_TYPE = os.environ.get('SESSION_TYPE', 'filesystem')
    SESSION_PERMANENT = os.environ.get('SESSION_PERMANENT', 'False').lower() == 'true'
    SESSION_USE_SIGNER = os.environ.get('SESSION_USE_SIGNER', 'True').lower() == 'true'
    SESSION_KEY_PREFIX = os.environ.get('SESSION_KEY_PREFIX', 'session')
    PERMANENT_SESSION_LIFETIME = int(os.environ.get('PERMANENT_SESSION_LIFETIME', 86400))  # 24 часа

    # Конфигурация Redis для сессий
    SESSION_REDIS_HOST = os.environ.get('SESSION_REDIS_HOST', '127.0.0.1')
    SESSION_REDIS_PORT = os.environ.get('SESSION_REDIS_PORT', '6379')
    SESSION_REDIS = redis.StrictRedis(
        host=SESSION_REDIS_HOST,
        port=SESSION_REDIS_PORT,
        password=os.environ.get('SESSION_REDIS_PASSWORD')
    )

    # Уровень логирования
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARNING').upper()

class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    DEBUG = False
    TESTING = False
    LOG_LEVEL = 'WARNING'
    SESSION_TYPE = 'redis'
