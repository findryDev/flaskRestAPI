import requests


def domoticzAPI(id):
    r = requests.get(f"http://192.168.0.4:8080/json.htm?type=devices&rid={id}")
    if r == 200:
        data = r.json()
        print(data)
        return data['result'][0]['Temp']
    else:
        return ('NONE')
domoticzAPI(7)