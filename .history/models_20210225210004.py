from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TemperatureModel(db.Model):
    __tablename__ = 'temperature'

    id = db.Column(db.Integer, primery_key=True)
    date = db.Column(db.DateTime)
    temperature = db.Column(db.Float)


