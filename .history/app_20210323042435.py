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
migrate = Migrate(app, db, compare_type=True)


class Apicheck:
    def checkingApiKey():
        try:
            if request.headers['keyApi'] == Config.APIAUTH:
                return {'check': True}
            else:
                return {'check': False, 'text': 'ACCESS DENY', 'status': 401}
        except KeyError as e:
            if e.args[0] == 'HTTP_KEYAPI':
                return {'check': False, 'text': 'ACCESS DENY', 'status': 401}
            else:
                return {'check': False, 'text': 'KEY ERROR', 'status': 400}


class TemperaturesView(Resource, Apicheck):
    def get(self):
        checkDict = Apicheck.checkingApiKey()
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
        checkDict = Apicheck.checkingApiKey()
        if checkDict['check']:
            data = request.get_json(force=True)
            if request.endpoint == "temperatures/sensor1":
                new_temperature = TemperatureModelSensor1(data['temperature'])
            if request.endpoint == "temperatures/sensor2":
                new_temperature = TemperatureModelSensor2(data['temperature'])
            if request.endpoint == "temperatures/sensor3":
                new_temperature = TemperatureModelSensor3(data['temperature'])
            db.session.add(new_temperature)
            db.session.commit()
            return {'temperature': data['temperature']}
        else:
            return checkDict['text'], checkDict['status']


class TemperatureView(Resource):
    def get(self):
        checkDict = Apicheck.checkingApiKey()
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
        checkDict = Apicheck.checkingApiKey()
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
    def getLastRecordToDict(tempModel):
        temperature = ((tempModel.
                        query.order_by(sqlalchemy.
                        desc(tempModel.id)).first()).
                        json())
        return temperature
    
    def getLastFiveRecordToDict(tempModel):
        temperatureLastFive = ((tempModel.query.order_by(sqlalchemy.
                                desc(tempModel.id)).limit(5).all()))
        temperatureLastFive.reverse()
        dictDateTemp = {}
        for x in temperatureLastFive:
            temporeDict = x.json()
            dictDateTemp.update(
                {temporeDict['date']: temporeDict['temperature']})
        return dictDateTemp
    
    temperatureS1 = getLastRecordToDict(TemperatureModelSensor1)
    temperatureS2 = getLastRecordToDict(TemperatureModelSensor2)
    temperatureS3 = getLastRecordToDict(TemperatureModelSensor3)
    
    temperaturesS1 = getLastFiveRecordToDict(TemperatureModelSensor1)
    temperaturesS2 = getLastFiveRecordToDict(TemperatureModelSensor2)
    temperaturesS3 = getLastFiveRecordToDict(TemperatureModelSensor3)
    

    return render_template("temperature.html",
                           temperatureS1=(f'{temperatureS1["date"]}\n\
                                           {temperatureS1["temperature"]}'),
                           temperatureS2=(f'{temperatureS2["date"]}\n\
                                           {temperatureS2["temperature"]}'),
                           temperatureS3=(f'{temperatureS3["date"]}\n\
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
    app.run(host='192.168.0.2', port=port)
    #app.run(host='127.0.0.1', port=port)
