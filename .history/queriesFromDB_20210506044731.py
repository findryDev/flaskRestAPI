import sqlalchemy

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
    temperatures1 = (modelDB.query.order_by(sqlalchemy.
                     desc(modelDB.id)).limit(howMany).all())
    temperatures1.reverse()
