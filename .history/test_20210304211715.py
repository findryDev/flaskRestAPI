import requests
import datetime as dt
import random


symTemp = (random.random() * 10) + 20
sendDate = {"DateTime": f"{str(dt.datetime.now())}", "temperature":symTemp}

r = requests.post('http://0.0.0.0:5000/temperatures',
                  data=sendDate)
print(r.text)