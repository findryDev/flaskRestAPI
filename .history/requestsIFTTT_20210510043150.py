import requests


def iftttOverheat(temp):
    event = "overheatCO"
    endPoint = f"https://maker.ifttt.com/trigger/{event}/with/key/lhdBTrM7E32TS7Jmgg1vBBY7ZNlznlzTdnbIATSCsiK"
    valueDict = {"value1": f"{temp}"}


    r = requests.post(endPoint, data=valueDict)
    print(r.status_code)


iftttOverheat(50)