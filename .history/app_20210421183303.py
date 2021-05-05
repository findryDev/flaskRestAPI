<<<<<<< HEAD
from flask import Flask, request, render_template
from flask_restful import Api, Resource
import sqlalchemy
from models import db, TemperatureModelSensor1
from models import TemperatureModelSensor2
from models import TemperatureModelSensor3
from flask_migrate import Migrate
from config import Config
from plot import bokeh_plot, CDN_js
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
    local_tz = pytz.timezone('Europe/Warsaw')

    def utc_to_local(utc_dt):
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

    def reduceTimePause(x, y):
        newListDate = []
        newListTemp = []

        newListStart = 0

        for i in range(len(x)-1):
            if (abs((x[i+1] - x[i]).total_seconds())) > 60*60*2:
                newListStart = i + 1

        for k in range(newListStart, len(x)):
            newListDate.append(x[k])
            newListTemp.append(y[k])

    return newListDate, newListTemp
    def getLastRecordToDict(tempModel):
        temperature = ((tempModel.
                       query.order_by(sqlalchemy.
                        desc(tempModel.id)).first()).
                       json())
        return temperature

    def getLastRecordsToDict(tempModel, howMany):
        temperatureLastFive = ((tempModel.query.order_by(sqlalchemy.
                                desc(tempModel.id)).limit(howMany).all()))
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

    def toPlotsDataSensor1(howMany):
        x = []
        y = []
        lastsElements = ((TemperatureModelSensor1.query.order_by(sqlalchemy.
                          desc(TemperatureModelSensor1.id)).limit(howMany).all()))
        lastsElements.reverse()
        dates = []
        temperatures = []
        for m in lastsElements:
            dates.append(utc_to_local(m.Date))
            temperatures.append(m.temperature)
        dates, temperatures = reduceTimePause(dates, temperatures)

        if len(x) <= howMany:
            x.append(dates)
        y.append(temperatures)





    models = [TemperatureModelSensor1,
              TemperatureModelSensor2,
              TemperatureModelSensor3]
    legendLabels = ["Sensor1", "Sensor2", "Sensor3"]

    scriptsDiv = []
    scriptsDiv.append(bokeh_plot([TemperatureModelSensor1], 100, ["Sensor1"],
                                 "Temperature sensor 1", colors=['blue']))
    scriptsDiv.append(bokeh_plot([TemperatureModelSensor2], 100, ["Sensor2"],
                                 "Temperature sensor 2", colors=['green']))
    scriptsDiv.append(bokeh_plot([TemperatureModelSensor3], 100, ["Sensor3"],
                                 "Temperature sensor 3", colors=['yellow']))
    scriptsDiv.append(bokeh_plot(models, 100, legendLabels,
                                 "All sensors temperature",
                                 colors=['blue', 'green', 'yellow']))

    return render_template("temperature.html",
                           temperatureS1=temperatureS1,
                           temperatureS2=temperatureS2,
                           temperatureS3=temperatureS3,
                           div1=scriptsDiv[0][1],
                           div2=scriptsDiv[1][1],
                           div3=scriptsDiv[2][1],
                           divAll=scriptsDiv[3][1],
                           script1=scriptsDiv[0][0],
                           script2=scriptsDiv[1][0],
                           script3=scriptsDiv[2][0],
                           scriptAll=scriptsDiv[3][0],
                           cdn=CDN_js())


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
    # app.run(host='127.0.0.1', port=port)
=======
from flask import Flask, request, render_template
from flask_restful import Api, Resource
import sqlalchemy
from models import db, TemperatureModelSensor1
from models import TemperatureModelSensor2
from models import TemperatureModelSensor3
from flask_migrate import Migrate
from config import Config
from plot import bokeh_plot, CDN_js
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
    local_tz = pytz.timezone('Europe/Warsaw')

    def utc_to_local(utc_dt):
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

    def reduceTimePause(x, y):
        newListDate = []
        newListTemp = []

        newListStart = 0

        for i in range(len(x)-1):
            if (abs((x[i+1] - x[i]).total_seconds())) > 60*60*2:
                newListStart = i + 1

        for k in range(newListStart, len(x)):
            newListDate.append(x[k])
            newListTemp.append(y[k])

    return newListDate, newListTemp
    def getLastRecordToDict(tempModel):
        temperature = ((tempModel.
                       query.order_by(sqlalchemy.
                        desc(tempModel.id)).first()).
                       json())
        return temperature

    def getLastRecordsToDict(tempModel, howMany):
        temperatureLastFive = ((tempModel.query.order_by(sqlalchemy.
                                desc(tempModel.id)).limit(howMany).all()))
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

    def toPlotsDataSensor1(howMany):
        x = []
        y = []
        lastsElements = ((TemperatureModelSensor1.query.order_by(sqlalchemy.
                          desc(TemperatureModelSensor1.id)).limit(howMany).all()))
        lastsElements.reverse()
        dates = []
        temperatures = []
        for m in lastsElements:
            dates.append(utc_to_local(m.Date))
            temperatures.append(m.temperature)
        dates, temperatures = reduceTimePause(dates, temperatures)

        if len(x) <= howMany:
            x.append(dates)
        y.append(temperatures)





    models = [TemperatureModelSensor1,
              TemperatureModelSensor2,
              TemperatureModelSensor3]
    legendLabels = ["Sensor1", "Sensor2", "Sensor3"]

    scriptsDiv = []
    scriptsDiv.append(bokeh_plot([TemperatureModelSensor1], 100, ["Sensor1"],
                                 "Temperature sensor 1", colors=['blue']))
    scriptsDiv.append(bokeh_plot([TemperatureModelSensor2], 100, ["Sensor2"],
                                 "Temperature sensor 2", colors=['green']))
    scriptsDiv.append(bokeh_plot([TemperatureModelSensor3], 100, ["Sensor3"],
                                 "Temperature sensor 3", colors=['yellow']))
    scriptsDiv.append(bokeh_plot(models, 100, legendLabels,
                                 "All sensors temperature",
                                 colors=['blue', 'green', 'yellow']))

    return render_template("temperature.html",
                           temperatureS1=temperatureS1,
                           temperatureS2=temperatureS2,
                           temperatureS3=temperatureS3,
                           div1=scriptsDiv[0][1],
                           div2=scriptsDiv[1][1],
                           div3=scriptsDiv[2][1],
                           divAll=scriptsDiv[3][1],
                           script1=scriptsDiv[0][0],
                           script2=scriptsDiv[1][0],
                           script3=scriptsDiv[2][0],
                           scriptAll=scriptsDiv[3][0],
                           cdn=CDN_js())


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
    # app.run(host='127.0.0.1', port=port)
>>>>>>> 0b75138e047af14274c183f7e76284f83985dc5d
