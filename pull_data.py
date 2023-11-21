import requests

""" API SETTINGS """

DIRECTORY = "data/"

f = open("key.txt", "r")
key = str(f.read())
# print(key,end='')
URL = "https://data.bordeaux-metropole.fr/geojson?key=" + key + "&typename=ci_vcub_p"
response = requests.get(URL)

#https://data.bordeaux-metropole.fr/geojson/aggregate/ST_PARK_P?key=[VOTRECLE]&filter={"ident":"CUBPK42"}&rangeStart=2023-11-19T00:00:00&rangeEnd=2023-11-20T00:00:00&rangeStep=hour&attributes={"libres":"average","total":"max"}

open(DIRECTORY + "dataset.json", "wb").write(response.content)