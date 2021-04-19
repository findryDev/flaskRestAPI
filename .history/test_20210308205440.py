import requests
import datetime as dt
import random
import time


while True:
    symTemp = (random.random() * 10) + 20
    sendDate = {"DateTime": f"{str(dt.datetime.now())}", "temperature":symTemp}

    r = requests.post('http://localhost:5432/temperatures',
                    json=sendDate)
    print(r.text)
