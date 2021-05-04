from flask import Flask, request, render_template
from flask_restful import Api, Resource
import sqlalchemy
from models import db, TemperatureModelSensor1
from models import TemperatureModelSensor2
from models import TemperatureModelSensor3
from flask_migrate import Migrate
from config import Config
from plot import bokeh_plot,  bokeh_plots, CDN_js
from requestDomoticz import getTempForDomoticzAPI
from requestApiWether import getCurrentWeather
import logging
import os

# create a custom logger foF

loggerError = logging.getLogger('flaskErr')
loggerError.setLevel(logging.ERROR)
loggerRequests = logging.getLogger('flaskRequests')
loggerRequests.setLevel(logging.DEBUG)


# create handlers

file_handler_err = logging.FileHandler('flaskErr.log')
file_handler_deb = logging.FileHandler('flaskDeb.log')

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

# add handler to the logger

loggerError.addHandler(file_handler_err)
loggerRequests.addHandler(file_handler_deb)


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
                    new_temperature = (TemperatureModelSensor1
                                       (data['temperature']))
                if request.endpoint == "temperatures/sensor2":
                    new_temperature = (TemperatureModelSensor2
                                       (data['temperature']))
                if request.endpoint == "temperatures/sensor3":
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
    return render_template("index.html")


refreshSiteCO = "30"
refreshSiteHome = "600"
howMany = 800
def getIconNameCO(temp):
    icon =""
    if temp <= 0:
        icon = "icon-thermometer-0"
    elif temp <= 20:
        icon = "icon-thermometer-quarter"
    elif temp  <= 40:
        icon ="icon-thermometer-2"
    elif temp <= 50:
        icon="icon-thermometer-3"
    elif icon <= 60:
        icon ="icon-thermometer"
    return icon

def getIconNameHome(temp):
    icon =""
    if temp <= 0:
        icon = "icon-thermometer-0"
    elif temp <= 10:
        icon = "icon-thermometer-quarter"
    elif temp  <= 15:
        icon ="icon-thermometer-2"
    elif temp <= 20:
        icon="icon-thermometer-3"
    elif icon <= 25:
        icon ="icon-thermometer"
    return icon

@app.route("/web/COtemperature")
def COtemperature():
    try:
        def getLastRecordToDict(tempModel):
            temperature = (tempModel.query.order_by(sqlalchemy.
                           desc(tempModel.id)).first().json())
            return temperature

        temperatureS1 = getLastRecordToDict(TemperatureModelSensor1)
        temperatureS2 = getLastRecordToDict(TemperatureModelSensor2)
        temperatureS3 = getLastRecordToDict(TemperatureModelSensor3)

        dataFormat = '%d-%m-%Y %H:%M:%S'
        temperatureS1['date'] = temperatureS1['date'].strftime(dataFormat)
        temperatureS2['date'] = temperatureS2['date'].strftime(dataFormat)
        temperatureS3['date'] = temperatureS3['date'].strftime(dataFormat)

        currentWeather = getCurrentWeather()

        loggerRequests.debug('flask requests')

        return render_template("COtemperature.html",
                               refresh=refreshSiteCO,
                               temperatureS1=temperatureS1,
                               temperatureS2=temperatureS2,
                               temperatureS3=temperatureS3,
                               currentWeatherText=currentWeather['currentWeatherText'],
                               currentWeatherTemperature=currentWeather['currentTemperature'],
                               currentWeatherObserv=currentWeather['observTime'])
    except Exception as e:
        loggerError.error(f'flask error: {e}')





@app.route("/web/COtemperature/kociol")
def tempKotla():
    try:
        def getLastRecordToDict(tempModel):
            temperature = (tempModel.query.order_by(sqlalchemy.
                           desc(tempModel.id)).first().json())
            return temperature

        temperatureS1 = getLastRecordToDict(TemperatureModelSensor1)
        temperatureS2 = getLastRecordToDict(TemperatureModelSensor2)
        temperatureS3 = getLastRecordToDict(TemperatureModelSensor3)

        dataFormat = '%d-%m-%Y %H:%M:%S'
        temperatureS1['date'] = temperatureS1['date'].strftime(dataFormat)
        temperatureS2['date'] = temperatureS2['date'].strftime(dataFormat)
        temperatureS3['date'] = temperatureS3['date'].strftime(dataFormat)

        temperatures1 = (TemperatureModelSensor1.query.order_by(sqlalchemy.
                         desc(TemperatureModelSensor1.id)).limit(howMany).all()
                         )
        temperatures1.reverse()

        scriptsDiv = []
        scriptsDiv.append(bokeh_plot(query=temperatures1,
                                     legend_label="Temperature sensor 1",
                                     title="Sensor 1",
                                     color='blue'))
        loggerRequests.debug('flask requests')
        return render_template("tempKotla.html",
                               refresh=refreshSiteCO,
                               temperatureS1=temperatureS1,
                               temperatureS2=temperatureS2,
                               temperatureS3=temperatureS3,
                               div1=scriptsDiv[0][1],
                               script1=scriptsDiv[0][0],
                               cdn=CDN_js())
    except Exception as e:
        loggerError.error(f'flask error: {e}')


@app.route("/web/COtemperature/wyjscie")
def tempWyjscie():
    try:
        def getLastRecordToDict(tempModel):
            temperature = (tempModel.query.order_by(sqlalchemy.
                           desc(tempModel.id)).first().json())
            return temperature

        temperatureS1 = getLastRecordToDict(TemperatureModelSensor1)
        temperatureS2 = getLastRecordToDict(TemperatureModelSensor2)
        temperatureS3 = getLastRecordToDict(TemperatureModelSensor3)

        dataFormat = '%d-%m-%Y %H:%M:%S'
        temperatureS1['date'] = temperatureS1['date'].strftime(dataFormat)
        temperatureS2['date'] = temperatureS2['date'].strftime(dataFormat)
        temperatureS3['date'] = temperatureS3['date'].strftime(dataFormat)

        temperatures2 = (TemperatureModelSensor2.query.order_by(sqlalchemy.
                         desc(TemperatureModelSensor2.id)).limit(howMany).all()
                         )
        temperatures2.reverse()

        scriptsDiv = []
        scriptsDiv.append(bokeh_plot(query=temperatures2,
                                     legend_label="Temperatura na wyjściu",
                                     title="Sensor 2",
                                     color='green'))

        loggerRequests.debug('flask requests')
        return render_template("tempWyjscie.html",
                               refresh=refreshSiteCO,
                               temperatureS1=temperatureS1,
                               temperatureS2=temperatureS2,
                               temperatureS3=temperatureS3,
                               div2=scriptsDiv[0][1],
                               script2=scriptsDiv[0][0],
                               cdn=CDN_js())
    except Exception as e:
        loggerError.error(f'flask error: {e}')


@app.route("/web/COtemperature/powrot")
def tempPowrot():
    try:
        def getLastRecordToDict(tempModel):
            temperature = (tempModel.query.order_by(sqlalchemy.
                           desc(tempModel.id)).first().json())
            return temperature

        temperatureS1 = getLastRecordToDict(TemperatureModelSensor1)
        temperatureS2 = getLastRecordToDict(TemperatureModelSensor2)
        temperatureS3 = getLastRecordToDict(TemperatureModelSensor3)

        dataFormat = '%d-%m-%Y %H:%M:%S'
        temperatureS1['date'] = temperatureS1['date'].strftime(dataFormat)
        temperatureS2['date'] = temperatureS2['date'].strftime(dataFormat)
        temperatureS3['date'] = temperatureS3['date'].strftime(dataFormat)

        temperatures3 = (TemperatureModelSensor3.query.order_by(sqlalchemy.
                         desc(TemperatureModelSensor3.id)).limit(howMany).all()
                         )
        temperatures3.reverse()

        scriptsDiv = []

        scriptsDiv.append(bokeh_plot(query=temperatures3,
                                     legend_label="Temperature sensor3",
                                     title="Sensor 3",
                                     color='yellow'))
        loggerRequests.debug('flask requests')
        return render_template("tempPowrot.html",
                               refresh=refreshSiteCO,
                               temperatureS1=temperatureS1,
                               temperatureS2=temperatureS2,
                               temperatureS3=temperatureS3,
                               div3=scriptsDiv[0][1],
                               script3=scriptsDiv[0][0],
                               cdn=CDN_js())
    except Exception as e:
        loggerError.error(f'flask error: {e}')


@app.route("/web/COtemperature/wszystkie")
def tempAll():
    try:
        def getLastRecordToDict(tempModel):
            temperature = (tempModel.query.order_by(sqlalchemy.
                           desc(tempModel.id)).first().json())
            return temperature

        temperatureS1 = getLastRecordToDict(TemperatureModelSensor1)
        temperatureS2 = getLastRecordToDict(TemperatureModelSensor2)
        temperatureS3 = getLastRecordToDict(TemperatureModelSensor3)

        dataFormat = '%d-%m-%Y %H:%M:%S'
        temperatureS1['date'] = temperatureS1['date'].strftime(dataFormat)
        temperatureS2['date'] = temperatureS2['date'].strftime(dataFormat)
        temperatureS3['date'] = temperatureS3['date'].strftime(dataFormat)
        temperatures1 = (TemperatureModelSensor1.query.order_by(sqlalchemy.
                         desc(TemperatureModelSensor1.id)).limit(howMany).all()
                         )
        temperatures1.reverse()

        temperatures2 = (TemperatureModelSensor2.query.order_by(sqlalchemy.
                         desc(TemperatureModelSensor2.id)).limit(howMany).all()
                         )
        temperatures2.reverse()

        temperatures3 = (TemperatureModelSensor3.query.order_by(sqlalchemy.
                         desc(TemperatureModelSensor3.id)).limit(howMany).all()
                         )
        temperatures3.reverse()

        temperaturesALL = [temperatures1, temperatures2, temperatures3]

        legendLabels = ["Sensor1", "Sensor2", "Sensor3"]
        scriptsDiv = []
        scriptsDiv.append(bokeh_plots(queries=temperaturesALL,
                                      legend_labels=legendLabels,
                                      titles="All sensors temperature",
                                      colors=['blue', 'green', 'yellow']))
        loggerRequests.debug('flask requests')
        return render_template("tempAll.html",
                               refresh=refreshSiteCO,
                               temperatureS1=temperatureS1,
                               temperatureS2=temperatureS2,
                               temperatureS3=temperatureS3,
                               divAll=scriptsDiv[0][1],
                               scriptAll=scriptsDiv[0][0],
                               cdn=CDN_js())
    except Exception as e:
        loggerError.error(f'flask error: {e}')


@app.route("/web/homeTemperature")
def homeTemperature():

    sypTemp = getTempForDomoticzAPI(3)
    jadTemp = getTempForDomoticzAPI(6)
    lazTemp = getTempForDomoticzAPI(7)
    kotTemp = getTempForDomoticzAPI(8)
    wejTemp = getTempForDomoticzAPI(36)

    return render_template('homeTemperature.html',
                           refresh=refreshSiteHome,
                           sypTemp=sypTemp,
                           jadTemp=jadTemp,
                           lazTemp=lazTemp,
                           kotTemp=kotTemp,
                           wejTemp=wejTemp)


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
