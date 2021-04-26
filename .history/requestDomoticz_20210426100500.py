import requests


username = 'ZmlsaXA='
password = 'Rm42OTYxMjk2MDc='


def auth():
    r = requests.get(f"http://192.168.0.4:8080/json.htm?username={username}&password={password}&api-call")
    return(r)

def domoticzAPI(id):
    r = requests.get(f"http://{username}:{password}@192.168.0.4:8080/json.htm?type=devices&rid={id}")
    if r == 200:
        data = r.json()
        print(data)
        return data['result'][0]['Temp']
    else:
        return ('NONE')

print(auth())