import requests
import datetime as dt
import random
import time


while True:
    symTemp = (random.random() * 10) + 20
    sendDate = {"DateTime": f"{str(dt.datetime.now())}", "temperature":symTemp}

    r = requests.post('https://wschodnia4.herokuapp.com/temperatures',
                    json=sendDate)
    print(r.text)
    time.sleep(10)