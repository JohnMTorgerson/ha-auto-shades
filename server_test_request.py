import requests
from pprint import pprint

url = 'http://192.168.2.200:5000/run_shades'
data = { "data": "testing" }

r = requests.post(url=url, json=data)

pprint(r.text)