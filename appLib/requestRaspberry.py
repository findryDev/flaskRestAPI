
'''
id of sensors pi
    id 14 - CPU temperature
    id 15 - GPU temperature
    id 16 - Memory usage
    id 17 - CPU usage
    id 18 - CPU speed
    id 23 - Connections
    id 28 - Domoticz memory
    id 19 - Up_time
    id 33 - Clock ARM
	id 34 - Clock V3D
    id 35 - Clock Core
'''

import requests

username = 'ZmlsaXA='
password = 'Rm42OTYxMjk2MDc='


def getRaspberryInfo():
    id_paramiter = [('temperature', '14'),
                    ('clockCPU', '33'),
                    ('usedRamPercent', '16'),
                    ('upTime', '19'),
                    ('info', '30')]
    results = {}
    for n in id_paramiter:
        endpoint = (("http://192.168.0.4:8080/json.htm?") +
                    (f"username={username}") +
                    (f"&password={password}&type=devices&rid={n[1]}"))
        r = requests.get(endpoint)
        if r.status_code == 200:
            data = r.json()
            results.update({n[0]: data['result'][0]["Data"]})
    return results


