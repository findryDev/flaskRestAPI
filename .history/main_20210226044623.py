from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from models import db, TemperatureModel

app = Flask(__name__)

api = Api(app)

if __name__ == '__main__':
    app.run(host='localhost', port='5000')