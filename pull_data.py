import requests

""" API SETTINGS """

DIRECTORY = "data/"

f = open("key.txt", "r")
key = str(f.read())
# print(key,end='')
URL = "https://data.bordeaux-metropole.fr/geojson?key=" + key + "&typename=ci_vcub_p&rangeStart=2023-11-10T00:00:00&rangeEnd=2023-11-20T00:00:00"
response = requests.get(URL)

if response.status_code == 200:
    open(DIRECTORY + "dataset.json", "wb").write(response.content)
    print("Données récupérées avec succès.")
else:
    print("Erreur lors de la récupération des données")