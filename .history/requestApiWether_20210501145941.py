import requests
import urllib.parse

locationName = 'dobrzeń mały'
urlNameLocation = urllib.parse.quote(locationName)
apiKey = 'bvEAnMf698TpZPea1xgrDFlgwJHiBs6n'
locationKey = "1410264"
getLocationKeyEndPoint = f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey={apiKey}&q={urlNameLocation}'
currnetWeatherEndPoint = f'http://dataservice.accuweather.com/currentconditions/v1/{locationKey}?apikey={apiKey}=pl'

print(getLocationKeyEndPoint)
r = requests.get('http://dataservice.accuweather.com/locations/v1/cities/search?apikey=bvEAnMf698TpZPea1xgrDFlgwJHiBs6n&q=dobrze%C5%84%20ma%C5%82y')
r
print(r.text)