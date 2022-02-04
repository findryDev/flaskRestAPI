
def getIconNameCO(temp):
    icon = ""
    if temp <= 10:
        icon = "icon-thermometer-0"
    elif temp > 10 and temp <= 20:
        icon = "icon-thermometer-quarter"
    elif temp > 20 and temp <= 40:
        icon = "icon-thermometer-2"
    elif temp > 40 and temp < 50:
        icon = "icon-thermometer-3"
    elif temp >= 50:
        icon = "icon-thermometer"
    return icon


def getIconNameHome(temp):
    icon = ""
    if temp <= 10:
        icon = "icon-thermometer-0"
    elif temp > 10 and temp <= 15:
        icon = "icon-thermometer-quarter"
    elif temp > 15 and temp <= 20:
        icon = "icon-thermometer-2"
    elif temp > 20 and temp < 25:
        icon = "icon-thermometer-3"
    elif temp >= 25:
        icon = "icon-thermometer"
    return icon


def get_temperature_trend(temp_delta):
    if temp_delta > 0:
        return 'icon-up'
    if temp_delta == 0:
        return 'icon-exchange'
    if temp_delta < 0:
        return 'icon-down'
