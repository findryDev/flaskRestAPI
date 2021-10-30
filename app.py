from flask import Flask, request, render_template
from flask_restful import Api, Resource
import sqlalchemy
from appLib.models import db
from appLib.models import TemperatureModelSensor1
from appLib.models import TemperatureModelSensor2
from appLib.models import TemperatureModelSensor3
from flask_migrate import Migrate
from appLib.common import cache
from config import Config
from appLib.plot import bokeh_plot,  bokeh_plots, CDN_js
from appLib.requestDomoticz import getTempForDomoticzAPI
from appLib.requestApiWether import getCurrentWeather
from appLib.queriesFromDB import sensorQueries, sensorQueriesToPlot
from appLib.queriesFromDB import deleteOldData
from appLib.requestsIFTTT import iftttOverheat
from appLib.appLogger import appLogger
from appLib.requestRaspberry import getRaspberryInfo
import os

appLogger = appLogger()
app = Flask(__name__)
cache.init_app(app=app,
               config={'CACHE_TYPE': 'filesystem',
                       'CACHE_DIR': '/tmp',
                       'CACHE_DEFAULT_TIMEOUT': 500,
                       'CACHE_IGNORE_ERRORS': True})

app.config.from_object('config.DevConfig')

api = Api(app)
db.init_app(app)
migrate = Migrate(app, db, compare_type=True)


refreshSiteCO = "30"
refreshSiteHome = "600"
dayLimitDB = 14
howManyRecords = 1600
overHeatTemp = 75

cache.set("overheatSensor1", None)
cache.set("overheatSensor2", None)
cache.set("overheatSensor3", None)


# function using in template
@app.context_processor
def utility_processor():
    def to_two_decimal(float_number):
        unity_digit, decimal_digit = str(float_number).split(".")
        if len(decimal_digit) < 2:
            decimal_digit = decimal_digit + "0"
        return unity_digit + "." + decimal_digit
    return dict(to_two_decimal=to_two_decimal)


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
        try:
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
                    dictDateTemp.update(
                        {str(x.date): x.temperature})
                appLogger.createDebLog()
                return dictDateTemp
            else:
                appLogger.createDebLog(checkDict['text'] + " " +
                                       checkDict['status'])
                return checkDict['text'], checkDict['status']
        except Exception as e:
            appLogger.createErrLog(e)

    def post(self):
        try:
            # date format dd.mm.yyyy hh:mm:ss
            checkDict = Apicheck.checkingApiKey()
            if checkDict['check']:
                data = request.get_json(force=True)

                appLogger.createDebLog()
                if request.endpoint == "temperatures/sensor1":
                    iftttOverheat(float(data['temperature']),
                                  float(overHeatTemp),
                                  "piec CO",
                                  "overheatSensor1")
                    deleteOldData(dayLimitDB, TemperatureModelSensor1)

                    # if delCount > 0: appLogger.createDBLog('del sensor1'
                    # , delCount)
                    new_temperature = TemperatureModelSensor1(
                        data['temperature'])
                if request.endpoint == "temperatures/sensor2":
                    iftttOverheat(float(data['temperature']),
                                  float(overHeatTemp),
                                  "wyjscie",
                                  "overheatSensor2")
                    deleteOldData(dayLimitDB, TemperatureModelSensor2)
                    # if delCount > 0: appLogger.createDBLog('del sensor2',
                    # len(data))
                    new_temperature = TemperatureModelSensor2(
                        data['temperature'])
                if request.endpoint == "temperatures/sensor3":
                    iftttOverheat(float(data['temperature']),
                                  float(overHeatTemp),
                                  "powrót",
                                  "overheatSensor3")
                    deleteOldData(dayLimitDB, TemperatureModelSensor3)
                    # if delCount > 0: appLogger.createDBLog('del sensor3',
                    # len(data))

                    new_temperature = TemperatureModelSensor3(
                        data['temperature'])
                db.session.add(new_temperature)
                db.session.commit()
                return {'temperature': data['temperature']}
            else:
                appLogger.createDebLog(checkDict['text'] + " " +
                                       checkDict['status'])
                return checkDict['text'], checkDict['status']

        except Exception as e:
            appLogger.createErrLog(e)


class TemperatureView(Resource):
    def get(self):
        try:
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
                appLogger.createDebLog()
                return {str(temperature.date): temperature.temperature}
            else:
                appLogger.createDebLog(checkDict['text'] + " " +
                                       checkDict['status'])
                return checkDict['text'], checkDict['status']
        except Exception as e:
            appLogger.createErrLog(e)


class TemperaturesDelete(Resource):
    def get(self):
        try:
            checkDict = Apicheck.checkingApiKey()
            if checkDict['check']:
                if request.endpoint == "deleteAll/sensor1":
                    delCount = (db.session.query(TemperatureModelSensor1)
                                .delete())
                    # appLogger.createDBLog('del sensor1', delCount)
                if request.endpoint == "deleteAll/sensor2":
                    delCount = (db.session.query(TemperatureModelSensor2)
                                .delete())
                    # appLogger.createDBLog('del sensor2', delCount)
                if request.endpoint == "deleteAll/sensor3":
                    delCount = (db.session.query(TemperatureModelSensor3)
                                .delete())
                    # appLogger.createDBLog('del sensor3', delCount)
                db.session.commit()
                return f"number of delete rows: {delCount}"
            else:
                appLogger.createDebLog(checkDict['text'] + " " +
                                       checkDict['status'])
                return checkDict['text'], checkDict['status']
        except Exception as e:
            appLogger.createErrLog(e)


@app.route("/")
def index():
    try:
        appLogger.createDebLog()
        return render_template("index.html")
    except Exception as e:
        appLogger.createErrLog(e)
        return render_template('error.html')


@app.route("/web/COtemperature")
def COtemperature():
    try:
        sensor1 = sensorQueries(TemperatureModelSensor1)
        sensor2 = sensorQueries(TemperatureModelSensor2)
        sensor3 = sensorQueries(TemperatureModelSensor3)

        currentWeather = getCurrentWeather()

        appLogger.createDebLog()

        return render_template("COtemperature.html",
                               refresh=refreshSiteCO,
                               sensor1=sensor1,
                               sensor2=sensor2,
                               sensor3=sensor3,
                               currentWeather=currentWeather)
    except Exception as e:
        appLogger.createErrLog(e)
        return render_template('error.html')


@app.route("/web/COtemperature/kociol")
def tempKotla():
    try:
        titleHead = 'Temperatura instalacji CO'
        titleBody = 'Temperatura kotła'
        mainURL = '/web/COtemperature/kociol'

        sensor1 = sensorQueries(TemperatureModelSensor1)
        sensor2 = sensorQueries(TemperatureModelSensor2)
        sensor3 = sensorQueries(TemperatureModelSensor3)

        temperatures1 = sensorQueriesToPlot(TemperatureModelSensor1,
                                            howManyRecords)

        scriptsDiv = []
        scriptsDiv.append(bokeh_plot(query=temperatures1,
                                     legend_label="Temperatura kotła",
                                     title="Temperatura kotła",
                                     color='blue'))
        appLogger.createDebLog()
        return render_template('tempCOtemplate.html',
                               titleHead=titleHead,
                               titleBody=titleBody,
                               mainURL=mainURL,
                               refresh=refreshSiteCO,
                               sensor1=sensor1,
                               sensor2=sensor2,
                               sensor3=sensor3,
                               divPlot=scriptsDiv[0][1],
                               scriptPlot=scriptsDiv[0][0],
                               cdn=CDN_js())
    except Exception as e:
        appLogger.createErrLog(e)
        return render_template('error.html')


@app.route("/web/COtemperature/wyjscie")
def tempWyjscie():
    try:
        titleHead = 'Temperatura instalacji CO'
        titleBody = 'Temperatura na wyjściu'
        mainURL = '/web/COtemperature/wyjscie'

        sensor1 = sensorQueries(TemperatureModelSensor1)
        sensor2 = sensorQueries(TemperatureModelSensor2)
        sensor3 = sensorQueries(TemperatureModelSensor3)

        temperatures2 = sensorQueriesToPlot(TemperatureModelSensor2,
                                            howManyRecords)

        scriptsDiv = []
        scriptsDiv.append(bokeh_plot(query=temperatures2,
                                     legend_label="Temperatura na wyjściu",
                                     title="Temperatura wyjście",
                                     color='green'))

        appLogger.createDebLog()
        return render_template('tempCOtemplate.html',
                               titleHead=titleHead,
                               titleBody=titleBody,
                               mainURL=mainURL,
                               refresh=refreshSiteCO,
                               sensor1=sensor1,
                               sensor2=sensor2,
                               sensor3=sensor3,
                               divPlot=scriptsDiv[0][1],
                               scriptPlot=scriptsDiv[0][0],
                               cdn=CDN_js())
    except Exception as e:
        appLogger.createErrLog(e)
        return render_template('error.html')


@app.route("/web/COtemperature/powrot")
def tempPowrot():
    try:
        titleHead = 'Temperatura instalacji CO'
        titleBody = 'Temperatura na powrocie'
        mainURL = '/web/COtemperature/powrot'

        sensor1 = sensorQueries(TemperatureModelSensor1)
        sensor2 = sensorQueries(TemperatureModelSensor2)
        sensor3 = sensorQueries(TemperatureModelSensor3)

        temperatures3 = sensorQueriesToPlot(TemperatureModelSensor3,
                                            howManyRecords)

        scriptsDiv = []

        scriptsDiv.append(bokeh_plot(query=temperatures3,
                                     legend_label="Temperatura powrót",
                                     title="Temperatura powrót",
                                     color='yellow'))
        appLogger.createDebLog()
        return render_template('tempCOtemplate.html',
                               titleHead=titleHead,
                               titleBody=titleBody,
                               mainURL=mainURL,
                               refresh=refreshSiteCO,
                               sensor1=sensor1,
                               sensor2=sensor2,
                               sensor3=sensor3,
                               divPlot=scriptsDiv[0][1],
                               scriptPlot=scriptsDiv[0][0],
                               cdn=CDN_js())
    except Exception as e:
        appLogger.createErrLog(e)
        return render_template('error.html')


@app.route("/web/COtemperature/wszystkie")
def tempAll():
    try:
        titleHead = 'Temperatura instalacji CO'
        titleBody = 'Wykres zbiorczy'
        mainURL = '/web/COtemperature/wszystkie'
        sensor1 = sensorQueries(TemperatureModelSensor1)
        sensor2 = sensorQueries(TemperatureModelSensor2)
        sensor3 = sensorQueries(TemperatureModelSensor3)

        temperatures1 = sensorQueriesToPlot(TemperatureModelSensor1,
                                            howManyRecords)
        temperatures2 = sensorQueriesToPlot(TemperatureModelSensor2,
                                            howManyRecords)
        temperatures3 = sensorQueriesToPlot(TemperatureModelSensor3,
                                            howManyRecords)

        temperaturesALL = [temperatures1, temperatures2, temperatures3]

        legendLabels = ["Kocioł", "Wyjscie", "Powrót"]
        scriptsDiv = []
        scriptsDiv.append(bokeh_plots(queries=temperaturesALL,
                                      legend_labels=legendLabels,
                                      titles="Temperatura instalacji",
                                      colors=['blue', 'green', 'yellow']))
        appLogger.createDebLog()

        return render_template("tempCOtemplate.html",
                               titleHead=titleHead,
                               titleBody=titleBody,
                               mainURL=mainURL,
                               refresh=refreshSiteCO,
                               sensor1=sensor1,
                               sensor2=sensor2,
                               sensor3=sensor3,
                               divPlot=scriptsDiv[0][1],
                               scriptPlot=scriptsDiv[0][0],
                               cdn=CDN_js())
    except Exception as e:
        appLogger.createErrLog(e)
        return render_template('error.html')


@app.route("/web/homeTemperature")
def homeTemperature():
    try:
        syp = getTempForDomoticzAPI(3)
        jad = getTempForDomoticzAPI(6)
        laz = getTempForDomoticzAPI(7)
        kot = getTempForDomoticzAPI(8)
        wej = getTempForDomoticzAPI(36)

        currentWeather = getCurrentWeather()
        appLogger.createDebLog()
        return render_template('homeTemperature.html',
                               refresh=refreshSiteHome,
                               syp=syp,
                               jad=jad,
                               laz=laz,
                               kot=kot,
                               wej=wej,
                               currentWeather=currentWeather)

    except Exception as e:
        appLogger.createErrLog(e)
        return render_template('error.html')


@app.route("/web/raspberryPi")
def piStatistic():
    try:
        raspberryPi = getRaspberryInfo()
        currentWeather = getCurrentWeather()
        appLogger.createDebLog()
        return render_template('raspberryPi.html',
                               refresh=refreshSiteHome,
                               pi=raspberryPi,
                               currentWeather=currentWeather)

    except Exception as e:
        appLogger.createErrLog(e)
        return render_template('error.html')


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
    app.run(host='0.0.0.0', port=port)
    # app.run(host='127.0.0.1', port=port)
