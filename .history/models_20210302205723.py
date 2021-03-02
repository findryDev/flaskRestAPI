from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class TemperatureModel(db.Model):
    __tablename__ = 'temperature'

    id = db.Column(db.Integer, primary_key=True)
    crDate = db.Column(db.String)
    temperature = db.Column(db.Float)

    def __init__(self, DateTime, temperature) -> None:
        self.crDate = DateTime
        self.temperature = temperature

    def json(self):
        return {'date': self.crDate, 'temperature': self.temperature}
