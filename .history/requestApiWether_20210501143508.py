import requests
import urllib.parse

locationName = 'dobrzeń mały'
urlNameLocation = urllib.parse.quote(locationName)
apiKey = 'bvEAnMf698TpZPea1xgrDFlgwJHiBs6n'
locationKey = "1410264"
getLocationKeyEndPoint = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={apiKey}={urlNameLocation}"
currnetWeatherEndPoint = f"http://dataservice.accuweather.com/currentconditions/v1/{locationKey}?apikey={apiKey}=pl"

r = requests.get(getLocationKeyEndPoint)

print(r.text)