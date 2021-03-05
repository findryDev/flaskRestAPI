import requests
import datetime as dt
import random
import time


for i in range(50):
    symTemp = (random.random() * 10) + 20
    sendDate = {"DateTime": f"{str(dt.datetime.now())}", "temperature":symTemp}

    r = requests.post('http://localhost:5000/temperatures',
                    json=sendDate)
    print(r.text)
    time.sleep(10)