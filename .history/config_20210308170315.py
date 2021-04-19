import os
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir,'.env'))


SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("DBUSERNAME")}:'\
                          f'{os.getenv("PASSWORD")}@'\
                          f'{os.getenv("SERVER")}:{os.getenv("PORT")}/'\
                          f'{os.getenv("DATABASE")}'

SQLALCHEMY_TRACK_MODIFICATIONS = 'False'