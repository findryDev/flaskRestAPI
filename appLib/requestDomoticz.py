import requests
from appLib.fontelloStyle import getIconNameHome

username = 'ZmlsaXA='
password = 'Rm42OTYxMjk2MDc='


def getTempForDomoticzAPI(id):
    results = {}
    endpoint = f"http://192.168.0.4:8080/json.htm?username={username}&password={password}&type=devices&rid={id}"
    r = requests.get(endpoint)
    if r.status_code == 200:
        data = r.json()
        icon = getIconNameHome(data['result'][0]['Temp'])
        results = {"temperature": data['result'][0]['Temp'],
                   "humidity": data['result'][0]['Humidity'],
                   "lastUpdate": data['result'][0]['LastUpdate'],
                   "batteryLevel": data['result'][0]['BatteryLevel'],
                   "icon": icon}

        return results
    else:
        return ('NONE', r.status_code)
