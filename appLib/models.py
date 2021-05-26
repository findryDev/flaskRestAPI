from flask_sqlalchemy import SQLAlchemy
import datetime
import pytz

local_tz = pytz.timezone('Europe/Warsaw')
db = SQLAlchemy()


def utc_to_local(utc_dt):
    print(utc_dt)
    print(type(utc_dt))

    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

# FIXME: change datetime to timestamp


class TemperatureModelSensor1(db.Model):
    __tablename__ = 'temperature_sensor1'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True),
                     default=datetime.datetime.utcnow,
                     onupdate=datetime.datetime.utcnow)
    temperature = db.Column(db.Float)

    def __init__(self, temperature):
        self.temperature = temperature

    def json(self):
        date = utc_to_local(self.date)
        return {'date': date, 'temperature': self.temperature}


class TemperatureModelSensor2(db.Model):
    __tablename__ = 'temperature_sensor2'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True),
                     default=datetime.datetime.utcnow,
                     onupdate=datetime.datetime.utcnow)
    temperature = db.Column(db.Float)

    def __init__(self, temperature):
        self.temperature = temperature

    def json(self):
        date = utc_to_local(self.date)
        return {'date': date, 'temperature': self.temperature}


class TemperatureModelSensor3(db.Model):
    __tablename__ = 'temperature_sensor3'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True),
                     default=datetime.datetime.utcnow,
                     onupdate=datetime.datetime.utcnow)
    temperature = db.Column(db.Float)

    def __init__(self, temperature):
        self.temperature = temperature

    def json(self):
        date = utc_to_local(self.date)
        return {'date': date, 'temperature': self.temperature}
