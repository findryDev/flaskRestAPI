import requests
import datetime as dt
import random


symTemp = (random.random() * 10) + 20


r = requests.post('localhost://temperatures',
                  data={f'{dt.datetime.now()}':symTemp}