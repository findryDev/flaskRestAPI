from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from models import db, TemperatureModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()

class TemperatureView(Resource):


if __name__ == '__main__':
    app.run(host='localhost', port='5000')