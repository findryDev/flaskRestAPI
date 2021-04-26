<<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy
import datetime
from dateutil import tz


db = SQLAlchemy()


def timeZoneConverting(dateToConvert):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Europe/Warsaw')
    utc = dateToConvert
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    return central.strftime("%d-%m-%y %H:%M:%S")


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
        date = timeZoneConverting(self.Date)
        return {'date': date, 'temperature': self.temperature}

    def toPlots(self, howMany):
        x = []
        y = []

        lastsElements = ((e.query.order_by(sqlalchemy.
                        desc(e.id)).limit(howMany).all()))
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
        date = timeZoneConverting(self.Date)
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
        date = timeZoneConverting(self.Date)
        return {'date': date, 'temperature': self.temperature}
=======
from flask_sqlalchemy import SQLAlchemy
import datetime
from dateutil import tz


db = SQLAlchemy()


def timeZoneConverting(dateToConvert):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Europe/Warsaw')
    utc = dateToConvert
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    return central.strftime("%d-%m-%y %H:%M:%S")


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
        date = timeZoneConverting(self.Date)
        return {'date': date, 'temperature': self.temperature}

    def toPlots(self, howMany):
        x = []
        y = []

        lastsElements = ((e.query.order_by(sqlalchemy.
                        desc(e.id)).limit(howMany).all()))
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
        date = timeZoneConverting(self.Date)
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
        date = timeZoneConverting(self.Date)
        return {'date': date, 'temperature': self.temperature}
>>>>>>> 0b75138e047af14274c183f7e76284f83985dc5d
