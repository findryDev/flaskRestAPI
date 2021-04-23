import requests
import datetime as dt
import random
import time



symTemp = (random.random() * 10) + 20
sendDate = {"DateTime": f"{str(dt.datetime.now())}", "temperature":symTemp}
headers = {'APIkey': '1234'}
r = requests.post('http://localhost:5432/temperatures',
                data=sendDate, headers= {'APIkey': '1234'})
print(r.text)
print(r.headers)
print(r)
