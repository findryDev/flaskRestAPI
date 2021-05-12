def getLastRecordToDict(tempModel):
            temperature = (tempModel.query.order_by(sqlalchemy.
                           desc(tempModel.id)).first().json())
            return temperature


def sensorQueries(ModelDB):
    temperatureQuery = getLastRecordToDict(ModelDB)

    dataFormat = '%d-%m-%Y %H:%M:%S'
    temperatureQuery['date'] = temperatureQuery['date'].strftime(dataFormat)

    return temperatureQuery
