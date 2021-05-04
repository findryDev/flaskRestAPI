import requests
import urllib.parse


def getCurrentWeather():
    locationName = 'dobrzeń mały'
    urlNameLocation = urllib.parse.quote(locationName)
    apiKey = 'bvEAnMf698TpZPea1xgrDFlgwJHiBs6n'
    getLocationKeyEndPoint = f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey={apiKey}&q={urlNameLocation}'
    locationKey = (requests.get(getLocationKeyEndPoint).json()[0]['Key'])
    currentWeatherEndPoint = f'http://dataservice.accuweather.com/currentconditions/v1/{locationKey}?apikey={apiKey}&language=pl'


    r = requests.get(currentWeatherEndPoint)
    jsonRespons = r.json()
    currentTemperature = jsonRespons[0]['Temperature']['Metric']['Value']
    currentWeatherText = jsonRespons[0]['WeatherText']
    observTime = jsonRespons[0]['LocalObservationDateTime']
    return(currentWeatherText, currentTemperature, observTime)


print(getCurrentWeather())