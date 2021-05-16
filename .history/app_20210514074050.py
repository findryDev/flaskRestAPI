from flask import Flask, request, render_template
from flask_restful import Api, Resource
import sqlalchemy
from models import db, TemperatureModelSensor1
from models import TemperatureModelSensor2
from models import TemperatureModelSensor3
from flask_migrate import Migrate
from common import cache
from config import Config
from plot import bokeh_plot,  bokeh_plots, CDN_js
from requestDomoticz import getTempForDomoticzAPI
from requestApiWether import getCurrentWeather
from fontelloStyle import getIconNameCO, getIconNameHome
from queriesFromDB import sensorQueries, sensorQueriesToPlot, deleteOldData
from requestsIFTTT import iftttOverheat
import logging
import os

# create a custom logger foF

loggerError = logging.getLogger('flaskErr')
loggerError.setLevel(logging.ERROR)
loggerRequests = logging.getLogger('flaskRequests')
loggerRequests.setLevel(logging.DEBUG)
loggerDB = logging.getLogger('dbOperation')
loggerDB.setLevel(logging.DEBUG)


# create handlers

file_handler_err = logging.FileHandler('flaskErr.log')
file_handler_deb = logging.FileHandler('flaskDeb.log')
file_handler_db = logging.FileHandler('dbLogger.log')

# create formatters and it to handlers

error_format = logging.Formatter('%(levelname)s'
                                 ' - %(asctime)s'
                                 ' - %(message)s'
                                 ' - %(name)s')
file_handler_err.setFormatter(error_format)

deb_format = logging.Formatter(' - %(asctime)s'
                               ' - %(message)s'
                               ' - %(name)s')
file_handler_deb.setFormatter(deb_format)

db_format = logging.Formatter(' - %(asctime)s'
                              ' - %(message)s'
                              ' - %(name)s'
                              ' - %(funcName)s')
file_handler_db.setFormatter(db_format)


# add handler to the logger

loggerError.addHandler(file_handler_err)
loggerRequests.addHandler(file_handler_deb)
loggerDB.addHandler(file_handler_db)

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
howMany = 800
overHeatTemp = 75

cache.set("overheatTime1", None)
cache.set("overheatTime2", None)
cache.set("overheatTime3", None)


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
                        {str(x.Date): x.temperature})
                loggerRequests.debug('flaskAPI GET requests')
                return dictDateTemp
            else:
                loggerRequests.debug('flaskAPI GET access deny')
                return checkDict['text'], checkDict['status']
        except Exception as e:
            loggerError.error(f'flaskAPI error: {e}')

    def post(self):
        try:
            # date format dd.mm.yyyy hh:mm:ss
            checkDict = Apicheck.checkingApiKey()
            if checkDict['check']:
                data = request.get_json(force=True)
                if request.endpoint == "temperatures/sensor1":
                    iftttOverheat(float(data['temperature']),
                                  float(overHeatTemp),
                                  "piec CO",
                                  "overheatTime1")
                    delCount = deleteOldData(dayLimitDB,
                                             TemperatureModelSensor1)
                    loggerDB.debug(f'deleted records:'
                                   f' {delCount}'
                                   f'in modelSensor1')
                    new_temperature = (TemperatureModelSensor1
                                       (data['temperature']))
                if request.endpoint == "temperatures/sensor2":
                    iftttOverheat(float(data['temperature']),
                                  float(overHeatTemp),
                                  "wyjscie",
                                  "overheatTime2")
                    delCount = deleteOldData(dayLimitDB,
                                             TemperatureModelSensor2)
                    loggerDB.debug(f'deleted records:'
                                   f'{delCount}'
                                   f'in modelSensor2')
                    new_temperature = (TemperatureModelSensor2
                                       (data['temperature']))
                if request.endpoint == "temperatures/sensor3":
                    iftttOverheat(float(data['temperature']),
                                  float(overHeatTemp),
                                  "powrót",
                                  "overheatTime3")
                    delCount = deleteOldData(dayLimitDB,
                                             TemperatureModelSensor3)
                    loggerDB.debug(f'deleted records:'
                                   f' {delCount}'
                                   f'in modelSensor3')
                    new_temperature = (TemperatureModelSensor3
                                       (data['temperature']))
                db.session.add(new_temperature)
                db.session.commit()
                return {'temperature': data['temperature']}
            else:
                return checkDict['text'], checkDict['status']
        except Exception as e:
            loggerError.error(f'flaskAPI error: {e}')


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
                loggerRequests.debug('flaskAPI GET one request')
                return {str(temperature.Date): temperature.temperature}
            else:
                loggerRequests.debug('flaskAPI GET access deny')
                return checkDict['text'], checkDict['status']
        except Exception as e:
            loggerError.error(f'flaskAPI error: {e}')


class TemperaturesDelete(Resource):
    def get(self):
        try:
            checkDict = Apicheck.checkingApiKey()
            if checkDict['check']:
                if request.endpoint == "deleteAll/sensor1":
                    delCount = (db.session.query(TemperatureModelSensor1)
                                .delete())
                if request.endpoint == "deleteAll/sensor2":
                    delCount = (db.session.query(TemperatureModelSensor2)
                                .delete())
                if request.endpoint == "deleteAll/sensor3":
                    delCount = (db.session.query(TemperatureModelSensor3)
                                .delete())
                db.session.commit()
                return f"number of delete rows: {delCount}"
            else:
                return checkDict['text'], checkDict['status']
        except Exception as e:
            loggerError.error(f'flaskAPI error: {e}')


@app.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        loggerError.error(f'flask error: {e}')
        return render_template('error.html')



@app.route("/web/COtemperature")
def COtemperature():
    try:
        temperatureS1 = sensorQueries(TemperatureModelSensor1)
        temperatureS2 = sensorQueries(TemperatureModelSensor2)
        temperatureS3 = sensorQueries(TemperatureModelSensor3)

        currentWeather = getCurrentWeather()

        loggerRequests.debug('flask requests')
        return render_template("COtemperature.html",
                               refresh=refreshSiteCO,
                               temperatureS1=temperatureS1,
                               temperatureS2=temperatureS2,
                               temperatureS3=temperatureS3,
                               iconS1=getIconNameCO(temperatureS1['temperature']),
                               iconS2=getIconNameCO(temperatureS2['temperature']),
                               iconS3=getIconNameCO(temperatureS3['temperature']),
                               currentWeatherText=currentWeather['currentWeatherText'],
                               currentWeatherTemperature=currentWeather['currentTemperature'],
                               currentWeatherObserv=currentWeather['observTime'])
    except Exception as e:
        loggerError.error(f'flask error: {e}')
        return render_template('error.html')


@app.route("/web/COtemperature/kociol")
def tempKotla():
    try:
        temperatureS1 = sensorQueries(TemperatureModelSensor1)
        temperatureS2 = sensorQueries(TemperatureModelSensor2)
        temperatureS3 = sensorQueries(TemperatureModelSensor3)

        temperatures1 = sensorQueriesToPlot(TemperatureModelSensor1, howMany)

        scriptsDiv = []
        scriptsDiv.append(bokeh_plot(query=temperatures1,
                                     legend_label="Temperatura kotła",
                                     title="Temperatura kotła",
                                     color='blue'))
        loggerRequests.debug('flask requests')
        return render_template("tempKotla.html",
                               refresh=refreshSiteCO,
                               temperatureS1=temperatureS1,
                               temperatureS2=temperatureS2,
                               temperatureS3=temperatureS3,
                               iconS1=getIconNameCO(temperatureS1['temperature']),
                               iconS2=getIconNameCO(temperatureS2['temperature']),
                               iconS3=getIconNameCO(temperatureS3['temperature']),
                               div1=scriptsDiv[0][1],
                               script1=scriptsDiv[0][0],
                               cdn=CDN_js())
    except Exception as e:
        loggerError.error(f'flask error: {e}')
        return render_template('error.html')


@app.route("/web/COtemperature/wyjscie")
def tempWyjscie():
    try:
        temperatureS1 = sensorQueries(TemperatureModelSensor1)
        temperatureS2 = sensorQueries(TemperatureModelSensor2)
        temperatureS3 = sensorQueries(TemperatureModelSensor3)

        temperatures2 = sensorQueriesToPlot(TemperatureModelSensor2, howMany)

        scriptsDiv = []
        scriptsDiv.append(bokeh_plot(query=temperatures2,
                                     legend_label="Temperatura na wyjściu",
                                     title="Temperatura wyjście",
                                     color='green'))

        loggerRequests.debug('flask requests')
        return render_template("tempWyjscie.html",
                               refresh=refreshSiteCO,
                               temperatureS1=temperatureS1,
                               temperatureS2=temperatureS2,
                               temperatureS3=temperatureS3,
                               iconS1=getIconNameCO(temperatureS1['temperature']),
                               iconS2=getIconNameCO(temperatureS2['temperature']),
                               iconS3=getIconNameCO(temperatureS3['temperature']),
                               div2=scriptsDiv[0][1],
                               script2=scriptsDiv[0][0],
                               cdn=CDN_js())
    except Exception as e:
        loggerError.error(f'flask error: {e}')
        return render_template('error.html')


@app.route("/web/COtemperature/powrot")
def tempPowrot():
    try:
        temperatureS1 = sensorQueries(TemperatureModelSensor1)
        temperatureS2 = sensorQueries(TemperatureModelSensor2)
        temperatureS3 = sensorQueries(TemperatureModelSensor3)

        temperatures3 = sensorQueriesToPlot(TemperatureModelSensor3, howMany)

        scriptsDiv = []

        scriptsDiv.append(bokeh_plot(query=temperatures3,
                                     legend_label="Temperatura powrót",
                                     title="Temperatura powrót",
                                     color='yellow'))
        loggerRequests.debug('flask requests')
        return render_template("tempPowrot.html",
                               refresh=refreshSiteCO,
                               temperatureS1=temperatureS1,
                               temperatureS2=temperatureS2,
                               temperatureS3=temperatureS3,
                               iconS1=getIconNameCO(temperatureS1['temperature']),
                               iconS2=getIconNameCO(temperatureS2['temperature']),
                               iconS3=getIconNameCO(temperatureS3['temperature']),
                               div3=scriptsDiv[0][1],
                               script3=scriptsDiv[0][0],
                               cdn=CDN_js())
    except Exception as e:
        loggerError.error(f'flask error: {e}')
        return render_template('error.html')


@app.route("/web/COtemperature/wszystkie")
def tempAll():
    try:
        temperatureS1 = sensorQueries(TemperatureModelSensor1)
        temperatureS2 = sensorQueries(TemperatureModelSensor2)
        temperatureS3 = sensorQueries(TemperatureModelSensor3)

        temperatures1 = sensorQueriesToPlot(TemperatureModelSensor1, howMany)
        temperatures2 = sensorQueriesToPlot(TemperatureModelSensor2, howMany)
        temperatures3 = sensorQueriesToPlot(TemperatureModelSensor3, howMany)

        temperaturesALL = [temperatures1, temperatures2, temperatures3]

        legendLabels = ["Sensor1", "Sensor2", "Sensor3"]
        scriptsDiv = []
        scriptsDiv.append(bokeh_plots(queries=temperaturesALL,
                                      legend_labels=legendLabels,
                                      titles="Temperatura instalacji",
                                      colors=['blue', 'green', 'yellow']))
        loggerRequests.debug('flask requests')
        return render_template("tempAll.html",
                               refresh=refreshSiteCO,
                               temperatureS1=temperatureS1,
                               temperatureS2=temperatureS2,
                               temperatureS3=temperatureS3,
                               iconS1=getIconNameCO(temperatureS1['temperature']),
                               iconS2=getIconNameCO(temperatureS2['temperature']),
                               iconS3=getIconNameCO(temperatureS3['temperature']),
                               divAll=scriptsDiv[0][1],
                               scriptAll=scriptsDiv[0][0],
                               cdn=CDN_js())
    except Exception as e:
        loggerError.error(f'flask error: {e}')
        return render_template('error.html')


@app.route("/web/homeTemperature")
def homeTemperature():
    try:
        sypTemp = getTempForDomoticzAPI(3)
        jadTemp = getTempForDomoticzAPI(6)
        lazTemp = getTempForDomoticzAPI(7)
        kotTemp = getTempForDomoticzAPI(8)
        wejTemp = getTempForDomoticzAPI(36)

        currentWeather = getCurrentWeather()

        return render_template('homeTemperature.html',
                            refresh=refreshSiteHome,
                            sypTemp=sypTemp,
                            jadTemp=jadTemp,
                            lazTemp=lazTemp,
                            kotTemp=kotTemp,
                            wejTemp=wejTemp,
                            iconS1=getIconNameHome(sypTemp[0]),
                            iconS2=getIconNameHome(jadTemp[0]),
                            iconS3=getIconNameHome(lazTemp[0]),
                            iconS4=getIconNameHome(kotTemp[0]),
                            iconS5=getIconNameHome(wejTemp[0]),
                            currentWeatherText=(currentWeather
                                                ['currentWeatherText']),
                            currentWeatherTemperature=(currentWeather
                                                        ['currentTemperature']),
                            currentWeatherObserv=(currentWeather
                                                    ['observTime']))
    except Exception as e:
        loggerError.error(f'flask error: {e}')
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
