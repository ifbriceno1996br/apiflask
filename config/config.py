from datetime import timedelta
from os import environ, path
from dotenv import load_dotenv
from config.settings import BASE_DIR_P

load_dotenv(path.join(BASE_DIR_P, '.env'))


class Config:
    ACCESS_EXPIRES = timedelta(hours=2)
    REFRESH_EXPIRES = timedelta(days=30)
    FLASK_DEBUG = False
    TESTING = False
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_ENV = environ.get('FLASK_ENV')
    JWT_SECRET_KEY = 'clavesecreta'
    JWT_TOKEN_LOCATION = ["headers", "cookies", "json", "query_string"]
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES


class DevConfig(Config):
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://postgres:Nomeacuerdo123.@192.168.100.95:5433/apiflask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    FLASK_DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
