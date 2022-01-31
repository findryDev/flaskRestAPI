import sqlalchemy
import datetime
from appLib.models import db
from appLib.fontelloStyle import getIconNameCO, get_temperature_trend


def getLastRecordToDict(tempModel):
    temperature = (tempModel.query.order_by(sqlalchemy.
                   desc(tempModel.id)).first().json())
    return temperature


def sensorQueries(modelDB):
    temperatureQuery = getLastRecordToDict(modelDB)

    dateFormat = '%d-%m-%Y %H:%M:%S'
    temperatureQuery['date'] = temperatureQuery['date'].strftime(dateFormat)
    icon = getIconNameCO(temperatureQuery['temperature'])
    trend = get_temperature_trend(get_temperature_delta(10, modelDB))
    temperatureQuery.update({"icon": icon})
    temperatureQuery.update({"trend": trend})
    temperatureQuery.update({"max": getMaxValue(modelDB)})
    temperatureQuery['max']['date'] = (temperatureQuery['max']['date'].
                                       strftime(dateFormat))
    temperatureQuery.update({"min": getMinValue(modelDB)})
    temperatureQuery['min']['date'] = (temperatureQuery['min']['date'].
                                       strftime(dateFormat))

    return temperatureQuery


def sensorQueriesToPlot(modelDB, howMany):
    temperatureQueries = (modelDB.query.order_by(sqlalchemy.
                          desc(modelDB.id)).limit(howMany).all())
    temperatureQueries.reverse()

    return temperatureQueries


def deleteOldData(daysLimit, model):
    try:
        oldPeriod = datetime.datetime.now() - datetime.timedelta(daysLimit)
        delCount = (db.session.query(model)
                    .filter(model.date <= oldPeriod).delete())
        db.session.commit()
        return delCount
    except Exception as e:
        return e

# TODO: add max and min function


def getMaxValue(model):
    max = (model.query.
           order_by(sqlalchemy.desc(model.temperature)).
           first().json())
    return max


def getMinValue(model):
    min = (model.query.
           order_by(sqlalchemy.asc(model.temperature)).
           first().json())
    return min


def get_temperature_delta(n, model):
    temp_list = []
    query = model.query.order_by(sqlalchemy.desc(model.id)).limit(n).all()
    query.reverse()
    trend = ""
    for e in query:
        temp_list.append(e.temperature)
    trend = temp_list[n-1] - (sum(temp_list)/len(temp_list))
    return trend
