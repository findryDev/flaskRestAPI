from flask import Flask, request, render_template
from flask_restful import Api, Resource
import sqlalchemy
from models import db, TemperatureModelSensor1
from models import TemperatureModelSensor2
from models import TemperatureModelSensor3
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
            if request.endpoint == "temperatures/sensor1":
                temperatures = TemperatureModelSensor1.query.all()
            if request.endpoint == "temperatures/sensor2":
                temperatures = TemperatureModelSensor2.query.all()
            if request.endpoint == "temperatures/sensor3":
                temperatures = TemperatureModelSensor3.query.all()
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
            if request.endpoint == "temperatures/sensor1":
                new_temperature = TemperatureModelSensor1(data['DateTime'],
                                                          data['temperature'])
            if request.endpoint == "temperatures/sensor2":
                new_temperature = TemperatureModelSensor2(data['DateTime'],
                                                          data['temperature'])
            if request.endpoint == "temperatures/sensor3":
                new_temperature = TemperatureModelSensor3(data['DateTime'],
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
            if request.endpoint == "temperature/sensor1":
                temperature = TemperatureModelSensor1.query.order_by(
                    sqlalchemy.desc(TemperatureModelSensor1.id)).first()
            if request.endpoint == "temperature/sensor2":
                temperature = TemperatureModelSensor2.query.order_by(
                    sqlalchemy.desc(TemperatureModelSensor2.id)).first()
            if request.endpoint == "temperature/sensor3":
                temperature = TemperatureModelSensor3.query.order_by(
                    sqlalchemy.desc(TemperatureModelSensor3.id)).first()
            dictDateTemp = {}
            temporeDict = temperature.json()
            dictDateTemp.update({temporeDict['date']:
                                temporeDict['temperature']})
            return dictDateTemp
        else:
            return checkDict['text'], checkDict['status']


class TemperaturesDelete(Resource):
    def get(self):
        checkDict = Apicheck.chekingApiKey()
        if checkDict['check']:
            if request.endpoint == "deleteAll/sensor1":
                delCount = db.session.query(TemperatureModelSensor1).delete()
            if request.endpoint == "deleteAll/sensor2":
                delCount = db.session.query(TemperatureModelSensor2).delete()
            if request.endpoint == "deleteAll/sensor3":
                delCount = db.session.query(TemperatureModelSensor3).delete()
            db.session.commit()
            return f"number of delete rows: {delCount}"
        else:
            return checkDict['text'], checkDict['status']


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/web/temperature")
def temperature():
    temperatureS1 = (TemperatureModelSensor1.
                     query.order_by(sqlalchemy.desc(TemperatureModelSensor1.id)).first()).json()
    temperatureS2 = (TemperatureModelSensor2.
                     query.order_by(sqlalchemy.desc(TemperatureModelSensor2.id)).first()).json()
    temperatureS3 = (TemperatureModelSensor3.
                     query.order_by(sqlalchemy.desc(TemperatureModelSensor3.id)).first()).json()
    return render_template("temperature.html",
                            temperatureS1=(f'{temperatureS1["date"]}:\
                                           {temperatureS1["temperature"]}'),
                            temperatureS2=(f'{temperatureS2["date"]}:\
                                           {temperatureS2["temperature"]}'),
                            temperatureS3=(f'{temperatureS3["date"]}:\
                                           {temperatureS3["temperature"]}'))



api.add_resource(TemperaturesView, '/api/temperatures/sensor1',
                 endpoint="temperatures/sensor1")
api.add_resource(TemperaturesView, '/api/temperatures/sensor2',
                 endpoint="temperatures/sensor2")
api.add_resource(TemperaturesView, '/api/temperatures/sensor3',
                 endpoint="temperatures/sensor3")
api.add_resource(TemperatureView, '/api/temperature/sensor1',
                 endpoint="temperature/sensor1")
api.add_resource(TemperatureView, '/api/temperature/sensor2',
                 endpoint="temperature/sensor2")
api.add_resource(TemperatureView, '/api/temperature/sensor3',
                 endpoint="temperature/sensor3")
api.add_resource(TemperaturesDelete, '/api/deleteAll/sensor1',
                 endpoint="deleteAll/sensor1")
api.add_resource(TemperaturesDelete, '/api/deleteAll/sensor2',
                 endpoint="deleteAll/sensor2")
api.add_resource(TemperaturesDelete, '/api/deleteAll/sensor3',
                 endpoint="deleteAll/sensor3")




if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    app.run(host='127.0.0.1', port=port)
