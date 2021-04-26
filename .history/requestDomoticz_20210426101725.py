import requests


username = 'ZmlsaXA='
password = 'Rm42OTYxMjk2MDc='


def domoticzAPI(id):
    endpoint = f"http://192.168.0.4:8080/json.htm?username={username}&password={password}&type=devices&rid={id}"
    r = requests.get(endpoint)
    if r.status_code == 200:
        data = r.json()
        return data['result'][0]['Temp']
    else:
        return ('NONE', r.status_code)
