import requests

http://domoticz-ip<:port>/json.htm?username=MkE=&password=OVM=&api-call
username = 'filip'
password = 'Fn696129607'
def domoticzAPI(id):
    r = requests.get(f"http://192.168.0.4:8080/json.htm?{username}=MkE=&{password}=OVM=&type=devices&rid={id}")
    if r == 200:
        data = r.json()
        print(data)
        return data['result'][0]['Temp']
    else:
        return ('NONE')