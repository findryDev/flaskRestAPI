from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class TemperatureModel(db.Model):
    __tablename__ = 'temperature'

    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime)
    temperature = db.Column(db.Float)

    def __init__(self, DateTime, temperature) -> None:
        self.Date = DateTime
        self.temperature = temperature

    def json(self):
        return {'date': self.Date, 'temperature': self.temperature}
