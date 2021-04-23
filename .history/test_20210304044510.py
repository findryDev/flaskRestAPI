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
r = requests.post('http://localhost:5000/temperatures',
                  data=sendDate)
print(r)