from flask_sqlalchemy import SQLAlchemy
import datetime
import pytz


local_tz = pytz.timezone('Europe/Warsaw')
db = SQLAlchemy()


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


def reduceTimePause(x, y):
    newListDate = []
    newListTemp = []

    newListStart = 0

    for i in range(len(x)-1):
        if (abs((x[i+1] - x[i]).total_seconds())) > 60*60*2:
            newListStart = i + 1

    for k in range(newListStart, len(x)):
        newListDate.append(x[k])
        newListTemp.append(y[k])

    return newListDate, newListTemp


class TemperatureModelSensor1(db.Model):
    __tablename__ = 'temperature_sensor1'

    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime,
                     default=datetime.datetime.utcnow,
                     onupdate=datetime.datetime.utcnow)
    temperature = db.Column(db.Float)

    def __init__(self, temperature):
        self.temperature = temperature

    def json(self):
        date = utc_to_local(self.Date)
        return {'date': date, 'temperature': self.temperature}

    def toPlots(self, howMany):
        x = []
        y = []

        lastsElements = ((self.db.query.order_by(sqlalchemy.desc(e.id)).limit(howMany).all()))
        lastsElements.reverse()
        dates = []
        temperatures = []
        for m in lastsElements:
            dates.append(utc_to_local(m.Date))
            temperatures.append(m.temperature)
        dates, temperatures = reduceTimePause(dates, temperatures)

        if len(x) <= howMany:
            x.append(dates)
        y.append(temperatures)
        return x,y

class TemperatureModelSensor2(db.Model):
    __tablename__ = 'temperature_sensor2'

    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime,
                     default=datetime.datetime.utcnow,
                     onupdate=datetime.datetime.utcnow)
    temperature = db.Column(db.Float)

    def __init__(self, temperature):
        self.temperature = temperature

    def json(self):
        date = utc_to_local(self.Date)
        return {'date': date, 'temperature': self.temperature}


class TemperatureModelSensor3(db.Model):
    __tablename__ = 'temperature_sensor3'

    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime,
                     default=datetime.datetime.utcnow,
                     onupdate=datetime.datetime.utcnow)
    temperature = db.Column(db.Float)

    def __init__(self, temperature):
        self.temperature = temperature

    def json(self):
        date = utc_to_local(self.Date)
        return {'date': date, 'temperature': self.temperature}
