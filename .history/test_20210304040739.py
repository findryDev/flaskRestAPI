import requests
import datetime as dt
import random

r = requests.post('localhost://temperatures',
                  data={f'{dt.datetime.now()}':})