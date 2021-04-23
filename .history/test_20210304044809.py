import requests
import datetime as dt
import random


symTemp = (random.random() * 10) + 20
print(symTemp)
print(str(dt.datetime.now()))
sendDate = {"DateTime": f"{str(dt.datetime.now())}", "temperature":symTemp}
for k in sendDate:
    print(k, sendDate[k])
print(sendDate)
g = requests.get('http://0.0.0.0:5000/temperatures')
print(g)
r = requests.post('http://0.0.0.0:5000/temperatures',
                  data=sendDate)
print(r)