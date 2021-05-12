def getLastRecordToDict(tempModel):
            temperature = (tempModel.query.order_by(sqlalchemy.
                           desc(tempModel.id)).first().json())
            return temperature

def sensorQueries(dict: NameModelDict ):
        temperatureS1 = getLastRecordToDict(TemperatureModelSensor1)
        temperatureS2 = getLastRecordToDict(TemperatureModelSensor2)
        temperatureS3 = getLastRecordToDict(TemperatureModelSensor3)

        dataFormat = '%d-%m-%Y %H:%M:%S'
        temperatureS1['date'] = temperatureS1['date'].strftime(dataFormat)
        temperatureS2['date'] = temperatureS2['date'].strftime(dataFormat)
        temperatureS3['date'] = temperatureS3['date'].strftime(dataFormat)