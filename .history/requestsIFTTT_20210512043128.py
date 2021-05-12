import requests
from common import cache


def iftttOverheat(temp: float, limitTemp: float, sensor, cacheValue):
    overheatTime = cache.get(f"{cacheValue}")
    if temp > limitTemp and overheatTime is None:
        iftttOverheat(temp)
        cache.set(f"{cacheValue}", False)
        event = "overheatCO"
        endPoint = f"https://maker.ifttt.com/trigger/{event}/with/key/lhdBTrM7E32TS7Jmgg1vBBY7ZNlznlzTdnbIATSCsiK"
        valueDict = {"value1": f"{temp}", "value2": f"{sensor}" }
        r = requests.post(endPoint, data=valueDict)
        return r.status_code

