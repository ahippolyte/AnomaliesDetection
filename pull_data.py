import requests

""" API SETTINGS """

DIRECTORY = "data/"

f = open("key.txt", "r")
key = str(f.read())
parameters = {
    "startDate": "2023-11-06", 
    "endDate": "2023-11-07",
    "step": "hour", #5min 15min 30min hour day week month
    "stations": [""],
    "categories": [""],
}
StartDate = ""
URL = "https://data.bordeaux-metropole.fr/geojson/aggregate/ci_vcub_p?key=" + key +\
      "&rangeStart=" + parameters["startDate"] + "&rangeEnd=" + parameters["endDate"] + "&rangeStep="+ parameters["step"] + \
      "&group=time%2Bgid"

response = requests.get(URL)

if response.status_code == 200:
    open(DIRECTORY + "dataset.json", "wb").write(response.content)
    print("Données récupérées avec succès.")
else:
    print("Erreur lors de la récupération des données")