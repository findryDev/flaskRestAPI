import requests
from common import cache

def chekingOverheat(temp, limitTemp, sensor):
    overheatTime = cache.get("overheatTime")
    if temp > limitTemp and overheatTime == None:
        iftttOverheat(float(data['temperature']))
        cache.set("overheatTime1", False )



def iftttOverheat(temp):
    event = "overheatCO"
    endPoint = f"https://maker.ifttt.com/trigger/{event}/with/key/lhdBTrM7E32TS7Jmgg1vBBY7ZNlznlzTdnbIATSCsiK"
    valueDict = {"value1": f"{temp}"}

    r = requests.post(endPoint, data=valueDict)
    print(r.status_code)
