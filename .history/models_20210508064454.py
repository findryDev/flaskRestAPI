from flask_sqlalchemy import SQLAlchemy
import datetime
import pytz

local_tz = pytz.timezone('Europe/Warsaw')
db = SQLAlchemy()


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


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

    def delete_expired(self):
        expiration_days = 181
        limit = datetime.datetime.now() - datetime.timedelta(days=expiration_days)
        db.query.filter(db.timestamp &lt;= limit).delete()
        db.session.commit()


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
