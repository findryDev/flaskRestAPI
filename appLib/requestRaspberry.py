# TODO: Backend raspberry pi: temperatura, cpu, GPU

from vcgencmd import Vcgencmd
import subprocess


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
