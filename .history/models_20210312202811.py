from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class TemperatureModelSensor1(db.Model):
    __tablename__ = 'temperature_sensor1'

    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.String)
    temperature = db.Column(db.Float)

    def __init__(self, DateTime, temperature) -> None:
        self.Date = DateTime
        self.temperature = temperature

    def json(self):
        return {'date': self.Date, 'temperature': self.temperature}

class TemperatureModelSensor2(db.Model):
    __tablename__ = 'temperature_sensor2'

    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.String)
    temperature = db.Column(db.Float)

    def __init__(self, DateTime, temperature) -> None:
        self.Date = DateTime
        self.temperature = temperature

    def json(self):
        return {'date': self.Date, 'temperature': self.temperature}


class TemperatureModelSensor3(db.Model):
    __tablename__ = 'temperature_sensor3'

    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.String)
    temperature = db.Column(db.Float)

    def __init__(self, DateTime, temperature) -> None:
        self.Date = DateTime
        self.temperature = temperature

    def json(self):
        return {'date': self.Date, 'temperature': self.temperature}
