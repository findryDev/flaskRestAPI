import requests


def iftttOverheat(temp):
    temp = ''
    event = "overheatCO"
    endPoint = f"https://maker.ifttt.com/trigger/{event}/with/key/lhdBTrM7E32TS7Jmgg1vBBY7ZNlznlzTdnbIATSCsiK"
    valueDict = {"value1": f"{v1}"}


    r = requests.post(endPoint, data=valueDict)
    print(r.status_code)