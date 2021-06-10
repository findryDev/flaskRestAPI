# TODO: Backend raspberry pi: temperatura, cpu, GPU
'''
    id 14 - CPU temperature	
    id 15 - GPU temperature	
    id 16 - Memory usage	
    id 17 - CPU usage	
    id 18 - CPU speed	
    id 23 - Connections	
    id 28 - Domoticz memory
    id 19 - Up time
    id 33 - Clock ARM
	id 34 - Clock V3D
    id 35 - Clock Core
'''

import requests

username = 'ZmlsaXA='
password = 'Rm42OTYxMjk2MDc='


def getTempForDomoticzAPI(id, paramiter):
    results = {}
    endpoint = (("http://192.168.0.4:8080/json.htm?") +
                (f"username={username}") +
                (f"&password={password}&type=devices&rid={id}"))
    r = requests.get(endpoint)
    if r.status_code == 200:
        data = r.json()
        results = {f'paramiter': }

        return results
    else:
        return ('NONE', r.status_code)

'''
def getRaspberryInfo():
    vcgm = Vcgencmd()
    temperaturePi = vcgm.measure_temp()
    clockCPU = vcgm.measure_clock('arm') // 1000000
    s = subprocess.check_output(['free', '-m'], text=True)
    lines = s.split('\n')
    ram = (int(lines[1].split()[1]), int(lines[1].split()[6]), int(lines[1].split()[3]))

    return {'temperature': temperaturePi,
            'clockCPU': clockCPU,
            'allRam': round(ram[0]/1000, 2),
            'availableRam': round(ram[1]/1000, 2),
            'freeRam': round(ram[2]/1000, 2),
            'usedRamPercent': round((ram[2]/ram[0]*100), 2)
            }
'''