import requests
import datetime as dt
import random
import time


for _ in range(25):
    symTemp = (random.random() * 10) + 20
    sendDate = {"DateTime": f"{str(dt.datetime.now())}",
                "temperature": symTemp}
    headers = {'APIkey': '1234'}
    r = requests.get('http://192.168.0.4/api/temperatures/sensor1', headers={'keyApi': '1234'})
    print(r.text)
    print(r)
    time.sleep(10)
