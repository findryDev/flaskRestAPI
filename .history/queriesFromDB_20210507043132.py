import sqlalchemy
import datetime
from models import TemperatureModelSensor1, TemperatureModelSensor2, TemperatureModelSensor3


def getLastRecordToDict(tempModel):
    temperature = (tempModel.query.order_by(sqlalchemy.
                    desc(tempModel.id)).first().json())
    return temperature


def sensorQueries(modelDB):
    temperatureQuery = getLastRecordToDict(modelDB)

    dataFormat = '%d-%m-%Y %H:%M:%S'
    temperatureQuery['date'] = temperatureQuery['date'].strftime(dataFormat)

    return temperatureQuery


def sensorQueriesToPlot(modelDB, howMany):
    temperatureQueries = (modelDB.query.order_by(sqlalchemy.
                          desc(modelDB.id)).limit(howMany).all())
    temperatureQueries.reverse()

    return temperatureQueries


def deleteOldData(days):
    oldPeriod = datetime.datetime.now() - datetime.timedelta(days)
    q = TemperatureModelSensor1.query.filter_by(Date<oldPeriod))

deleteOldData(30)