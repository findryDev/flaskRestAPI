from os import environ, path, getenv
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    SQLALCHEMY_DATABASE_URI = f'postgresql://{getenv("DBUSERNAME")}:'\
                            f'{getenv("PASSWORD")}@'\
                            f'{getenv("SERVER")}:{getenv("PORT")}/'\
                            f'{getenv("DATABASE")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
    APIAUTH = getenv("APIAUTH")


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False



class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
