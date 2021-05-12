import requests
from common import cache


def iftttOverheat(temp: float, limitTemp: float, sensor):
    overheatTime = cache.get("overheatTime")
    if temp > limitTemp and overheatTime is None:
        iftttOverheat(temp)
        cache.set("overheatTime1", False)
        event = "overheatCO"
        endPoint = f"https://maker.ifttt.com/trigger/{event}/with/key/lhdBTrM7E32TS7Jmgg1vBBY7ZNlznlzTdnbIATSCsiK"
        valueDict = {"value1": f"{temp}", "value2": f"{sensor}" }
        r = requests.post(endPoint, data=valueDict)
        return r.status_code

