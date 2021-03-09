from os import environ, path, getenv
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


SQLALCHEMY_DATABASE_URI = f'postgresql://{getenv("DBUSERNAME")}:'\
                          f'{getenv("PASSWORD")}@'\
                          f'{getenv("SERVER")}:{getenv("PORT")}/'\
                          f'{getenv("DATABASE")}'

SQLALCHEMY_TRACK_MODIFICATIONS = 'False'