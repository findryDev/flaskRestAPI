import sqlalchemy
import datetime


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
    print(datetime.datetime.now() - datetime.timedelta(5))


deleteOldData(5)