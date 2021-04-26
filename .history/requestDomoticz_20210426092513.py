import requests


def domoticzAPI(id):
    r = requests.get(f"http://192.168.0.4:8080/json.htm?type=devices&rid={id}")
    data = r.json()
    return(data['result'][0]['Temp'])

print(domoticzAPI(7))