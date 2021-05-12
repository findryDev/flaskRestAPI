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
    qa = model.query.all()
    q = model.query.filter(model.Date > oldPeriod).all()
    print(q[0].Date)
    print(q[1].Date)
    print(q[2].Date)
    print(qa[0].Date)
    print(qa[1].Date)
    print(qa[2].Date)

    i = 0
    print(len(q))
    print(len(qa))
    i = db.session.query(model.query.filter(model.Date > oldPeriod).all()).delete()
    db.session.commit()
    return i

