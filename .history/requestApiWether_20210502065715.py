import requests
import urllib.parse

'''
{'location': {'name': 'Dobrzen Maly', 'region': '', 'country': 'Poland', 'lat': 50.75, 'lon': 17.87, 'tz_id': 'Europe/Warsaw', 'localtime_epoch': 1619884017, 'localtime': '2021-05-01 17:46'},
'current': {'last_updated_epoch': 1619883900, 'last_updated': '2021-05-01 17:45', 'temp_c': 12.0, 'temp_f': 53.6, 'is_day': 1,
'condition': {'text': 'Partly cloudy', 'icon': '//cdn.weatherapi.com/weather/64x64/day/116.png', 'code': 1003}, 'wind_mph': 6.9, 'wind_kph': 11.2, 'wind_degree': 70, 'wind_dir': 'ENE', 'pressure_mb': 1012.0, 'pressure_in': 30.4, 'precip_mm': 0.7, 'precip_in': 0.03, 'humidity': 71, 'cloud': 75, 'feelslike_c': 11.2, 'feelslike_f': 52.2, 'vis_km': 10.0, 'vis_miles': 6.0, 'uv': 2.0, 'gust_mph': 7.4, 'gust_kph': 11.9}}
'''



def getCurrentWeatherAcc():
    locationName = 'dobrzeń mały'
    urlNameLocation = urllib.parse.quote(locationName)
    apiKey = 'bvEAnMf698TpZPea1xgrDFlgwJHiBs6n'
    getLocationKeyEndPoint = f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey={apiKey}&q={urlNameLocation}'
    print(requests.get(getLocationKeyEndPoint).json())
    locationKey = (requests.get(getLocationKeyEndPoint).json()[0]['Key'])



    currentWeatherEndPoint = f'http://dataservice.accuweather.com/currentconditions/v1/{locationKey}?apikey={apiKey}&language=pl'


    r = requests.get(currentWeatherEndPoint)
    jsonRespons = r.json()
    currentTemperature = jsonRespons[0]['Temperature']['Metric']['Value']
    currentWeatherText = jsonRespons[0]['WeatherText']
    observTime = jsonRespons[0]['LocalObservationDateTime']
    return(currentWeatherText, currentTemperature, observTime)


def getCurrentWeatherWA():
    locationName = 'dobrzen maly'
    apiKey = 'e9b6674c95b4432695c152909210105'
    getCurrentWeatherApi = f'http://api.weatherapi.com/v1/current.json?key={apiKey}&q={locationName}&aqi=yes&lang=pl'
    print(getCurrentWeatherApi)
    r = requests.get(getCurrentWeatherApi).json()
    currentTemperature = r['current']['temp_c']
    currentWeatherText = r['current']['condition']['text']
    iconWeather = r['current']['condition']['icon']
    windKMH = r['current']['wind_kph']
    observTime = r['current']['last_updated']
    pm25 = round(r['current']['air_quality']['pm2_5'],2)
    pm10 = round(r['current']['air_quality']['pm10'],2)
    return(currentWeatherText, currentTemperature, iconWeather, wind_kph,
           observTime, pm25, pm10)


print(getCurrentWeatherWA())