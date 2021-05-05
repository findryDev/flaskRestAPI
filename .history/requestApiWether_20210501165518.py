import requests
import urllib.parse

def getCurrentWeather():
    locationName = 'dobrzeń mały'
    urlNameLocation = urllib.parse.quote(locationName)
    apiKey = 'bvEAnMf698TpZPea1xgrDFlgwJHiBs6n'
    locationKey = (requests.
                get('http://dataservice.accuweather.com/locations/v1/cities/search?apikey=bvEAnMf698TpZPea1xgrDFlgwJHiBs6n&q=dobrze%C5%84%20ma%C5%82y').
                json()[0]['Key'])
    getLocationKeyEndPoint = f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey={apiKey}&q={urlNameLocation}'
    currnetWeatherEndPoint = f'http://dataservice.accuweather.com/currentconditions/v1/{locationKey}?apikey={apiKey}&language=pl'


    r = requests.get(currnetWeatherEndPoint)
    jsonRespons = r.json()
    currentTemperature = jsonRespons[0]['Temperature']['Metric']['Value']
    currentWeatherText = jsonRespons[0]['WeatherText']
    observTime = jsonRespons[0]['LocalObservationDateTime']
    return(currentWeatherText, currentTemperature, observTime)