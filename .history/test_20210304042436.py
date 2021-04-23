import requests
import datetime as dt
import random


symTemp = (random.random() * 10) + 20
print(symTemp)
print(str(dt.datetime.now()))

r = requests.post('http://localhost:5000/temperatures',
                  data={f'{str(dt.datetime.now())}':symTemp})
