import requests

v1 = ''
event = "overheatCO"
endPoint = f"https://maker.ifttt.com/trigger/{event}/with/key/lhdBTrM7E32TS7Jmgg1vBBY7ZNlznlzTdnbIATSCsiK"
valueDict = {"value1" : f"{v1}"}

payload = {'key1': 'value1', 'key2': 'value2'}

r = requests.post("https://httpbin.org/post", data=payload)
print(r.text)