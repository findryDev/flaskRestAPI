import requests
from appLib.common import cache


def iftttOverheat(temp: float, limitTemp: float, sensor, cacheValue):
    overheatTime = cache.get(f"{cacheValue}")
    if temp > limitTemp and overheatTime is None:
        event = "overheatCO"
        endPoint = ((f"https://maker.ifttt.com/trigger/{event}") +
                    ("/with/key/lhdBTrM7E32TS7Jmgg1vBBY7ZNlznlzTdnbIATSCsiK"))
        valueDict = {"value1": f"{temp}", "value2": f"{sensor}"}
        r = requests.post(endPoint, data=valueDict)
        if r.status_code == 200:
            cache.set(f"{cacheValue}", False)
        return r.status_code
