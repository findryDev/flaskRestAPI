from flask import Flask, request
from flask_restful import Api, Resource
import sqlalchemy
from models import db, TemperatureModel
import os
import datetime as dt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


class TemperaturesView(Resource):
    def get(self):
        temperatures = TemperatureModel.query.all()
        dictDateTemp = {}
        for x in temperatures:
            temporeDict = x.json()
            dictDateTemp.update(
                {temporeDict['date']: temporeDict['temperature']})
        return dictDateTemp

    def post(self):
        # date format dd.mm.yyyy hh:mm:ss
        date = request.get_json(force=True)
        strDT = data['DateTime']
        dateTime = dt.datetime(year= int(strDT[6:9]),
                               month= int(strDT[3:4]),
                               day= int(strDT[0:1]),
                               hour= int(strDT[11:12]),
                               minute= int(strDT[14:15]),
                               second= int(strDT[17:18])

        new_temperature = TemperatureModel(data['DateTime'], data['temperature'])
        db.session.add(new_temperature)
        db.session.commit()
        return new_temperature.json()


class TemperatureView(Resource):
    def get(self):
        temperature = TemperatureModel.query.order_by(
            sqlalchemy.desc(TemperatureModel.id)).first()
        dictDateTemp = {}
        temporeDict = temperature.json()
        dictDateTemp.update({temporeDict['date']: temporeDict['temperature']})
        return dictDateTemp


api.add_resource(TemperaturesView, '/temperatures')
api.add_resource(TemperatureView, '/temperature')

app.debug = True
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
