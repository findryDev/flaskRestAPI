import sqlalchemy
import datetime
from models import db
from fontelloStyle import getIconNameCO


def getLastRecordToDict(tempModel):
    temperature = (tempModel.query.order_by(sqlalchemy.
                   desc(tempModel.id)).first().json())
    return temperature


def sensorQueries(modelDB):
    temperatureQuery = getLastRecordToDict(modelDB)

    dataFormat = '%d-%m-%Y %H:%M:%S'
    temperatureQuery['date'] = temperatureQuery['date'].strftime(dataFormat)
    icon = getIconNameCO(temperatureQuery['temperature'])
    temperatureQuery.update({"icon": icon})
    return temperatureQuery


def sensorQueriesToPlot(modelDB, howMany):
    temperatureQueries = (modelDB.query.order_by(sqlalchemy.
                          desc(modelDB.id)).limit(howMany).all())
    temperatureQueries.reverse()

    return temperatureQueries


def deleteOldData(daysLimit, model):
    oldPeriod = datetime.datetime.now() - datetime.timedelta(daysLimit)
    delCount = db.session.query(model).filter(model.Date <= oldPeriod).delete()
    db.session.commit()
    return delCount

