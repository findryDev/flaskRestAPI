import requests



apiKey = "bvEAnMf698TpZPea1xgrDFlgwJHiBs6n"
locationKey = "1410264"
getLocationKeyEndPoint = "http://dataservice.accuweather.com/locations/v1/cities/search?apikey=bvEAnMf698TpZPea1xgrDFlgwJHiBs6n&q=dobrze%C5%84%20ma%C5%82y"
currnetWeatherEndPoint = f"http://dataservice.accuweather.com/currentconditions/v1/{locationKey}}?apikey={apiKey}=pl"

r = requests.get(get)