def getLastRecordToDict(tempModel):
            temperature = (tempModel.query.order_by(sqlalchemy.
                           desc(tempModel.id)).first().json())
            return temperature


def sensorQueries(NameModelDict: dict ):
    temperatureQuery = getLastRecordToDict(NameModelDict['model'])

    dataFormat = '%d-%m-%Y %H:%M:%S'
    temperatureQuery['date'] = temperatureQuery['date'].strftime(dataFormat)

    return temperatureQuery
