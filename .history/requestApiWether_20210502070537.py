import requests


def getCurrentWeather():
    locationName = 'dobrzen maly'
    apiKey = 'e9b6674c95b4432695c152909210105'
    getCurrentWeatherApi = (f'http://api.weatherapi.com/v1/current.json?key={apiKey}&q={locationName}&aqi=yes&lang=pl')
    r = requests.get(getCurrentWeatherApi).json()
    weather = {'currentTemperature': r['current']['temp_c'],
               'currentWeatherText': r['current']['condition']['text'],
               'iconWeather': r['current']['condition']['icon'],
               'windKMH': r['current']['wind_kph'],
               'observTime': r['current']['last_updated'],
               'pm25': round(r['current']['air_quality']['pm2_5'], 2),
               'pm10': round(r['current']['air_quality']['pm10'], 2),
               }

    return(weather)


