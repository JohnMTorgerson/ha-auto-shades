import requests
from pprint import pprint

dir = ""
while dir != "up" and dir != "down":
    if dir != "" :
        print("Must enter either 'up' or 'down")
    dir = input("Enter 'up' or 'down': ")

url = 'http://192.168.2.200:5000/run_shades'
data = { "dir": dir }

r = requests.post(url=url, json=data)

pprint(f"Server response ::: {r.text}")