import sqlalchemy
import datetime
from models import db


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


def deleteOldData(days, model):
    oldPeriod = datetime.datetime.now() - datetime.timedelta(days)
    q = model.query.filter(model.Date > oldPeriod).all()
    i = 0
    for element in q:
        if element is not None:
            i = i + db.session.delete(element)
            db.session.commit()
    return i
