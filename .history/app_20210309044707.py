from flask import Flask, request
from flask_restful import Api, Resource
import sqlalchemy
from models import db, TemperatureModel
from flask_migrate import Migrate
from config import Config
import os


app = Flask(__name__)
app.config.from_object('config.DevConfig')

api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)


class TemperaturesView(Resource):
    def get(self):
        try :
            if request.headers['keyApi'] == Config.APIAUTH:
                temperatures = TemperatureModel.query.all()
                dictDateTemp = {}
                for x in temperatures:
                    temporeDict = x.json()
                    dictDateTemp.update(
                        {temporeDict['date']: temporeDict['temperature']})
                return dictDateTemp
            else:
                return "ACCESS DENY", 400
        except KeyError as e:
            if e == 'HTTP_KEYAPI':
                return "ACCESS DENY", 400
            else:
                return 'KEY ERROR', 400
    def post(self):
        # date format dd.mm.yyyy hh:mm:ss
        if request.headers['keyApi'] == Config.APIAUTH:
            data = request.get_json(force=True)
            new_temperature = TemperatureModel(data['DateTime'], data['temperature'])
            db.session.add(new_temperature)
            db.session.commit()
            return new_temperature.json()
        else:
            return "ACCESS DENY", 400


class TemperatureView(Resource):
    def get(self):
        if request.headers['keyApi'] == Config.APIAUTH:
            temperature = TemperatureModel.query.order_by(
                sqlalchemy.desc(TemperatureModel.id)).first()
            dictDateTemp = {}
            temporeDict = temperature.json()
            dictDateTemp.update({temporeDict['date']: temporeDict['temperature']})
            return dictDateTemp
        else:
            return "ACCESS DENY", 400


api.add_resource(TemperaturesView, '/temperatures')
api.add_resource(TemperatureView, '/temperature')

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    app.run(host='0.0.0.0', port=port)