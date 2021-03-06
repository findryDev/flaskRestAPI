from dotenv import load_dotenv
from flask import Flask, request
from flask_restful import Api, Resource
import sqlalchemy
from models import db, TemperatureModel
from flask_migrate import Migrate
import os
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("DBUSERNAME")}:'\
                                        f'{os.getenv("PASSWORD")}@'\
                                        f'{os.getenv("SERVER")}:{os.getenv("PORT")}/'\
                                        f'{os.getenv("DATABASE")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)


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
        data = request.get_json(force=True)
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

app.debug = os.environ.get('DEBUG_VALUE', 'True')
if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    app.run(host='localhost', port=port)
