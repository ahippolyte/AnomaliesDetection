import pandas as pd
import json

""" SETTINGS """

DIRECTORY = "data/"
DATASET = "dataset.json"

""" PARSE """
with open(DIRECTORY + DATASET, "r") as read_file:
    jsonfile = json.load(read_file)

df = pd.DataFrame()

for feature in jsonfile["features"]:
    print(feature['properties']['mdate'])
