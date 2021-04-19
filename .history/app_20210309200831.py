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


class Apicheck:
    def chekingApiKey():
        try:
            if request.headers['keyApi'] == Config.APIAUTH:
                return {'check': True}
            else:
                return {'check': False, 'text': 'ACCESS DENY', 'status': 400}
        except KeyError as e:
            if e.args[0] == 'HTTP_KEYAPI':
                return {'check': False, 'text': 'ACCESS DENY', 'status': 400}
            else:
                return {'check': False, 'text': 'KEY ERROR', 'status': 400}


class TemperaturesView(Resource, Apicheck):
    def get(self):
        checkDict = Apicheck.chekingApiKey()
        if checkDict['check']:
            temperatures = TemperatureModel.query.all()
            dictDateTemp = {}
            for x in temperatures:
                temporeDict = x.json()
                dictDateTemp.update(
                    {temporeDict['date']: temporeDict['temperature']})
            return dictDateTemp
        else:
            return checkDict['text'], checkDict['status']

    def post(self):
        # date format dd.mm.yyyy hh:mm:ss
        checkDict = Apicheck.chekingApiKey()
        if checkDict['check']:
            data = request.get_json(force=True)
            new_temperature = TemperatureModel(data['DateTime'],
                                               data['temperature'])
            db.session.add(new_temperature)
            db.session.commit()
            return new_temperature.json()
        else:
            return checkDict['text'], checkDict['status']


class TemperatureView(Resource):
    def get(self):
        checkDict = Apicheck.chekingApiKey()
        if checkDict['check']:
            temperature = TemperatureModel.query.order_by(
                sqlalchemy.desc(TemperatureModel.id)).first()
            dictDateTemp = {}
            temporeDict = temperature.json()
            dictDateTemp.update({temporeDict['date']:
                                temporeDict['temperature']})
            return dictDateTemp
        else:
            return checkDict['text'], checkDict['status']


class TemperatureDelete(Resource):
    def get(self):
        checkDict = Apicheck.chekingApiKey()
        if checkDict['check']:
            delCount = db.session.query(TemperatureModel).delete()
            db.session.commit()
            return
        else:
            return checkDict['text'], checkDict['status']


api.add_resource(TemperaturesView, '/temperatures')
api.add_resource(TemperatureView, '/temperature')

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    app.run(host='0.0.0.0', port=port)


