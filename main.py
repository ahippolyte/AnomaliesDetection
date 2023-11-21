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
    # for var in feature:
    #     print(var)
    # break
    # new_row = {'Courses':'Hyperion', 'Fee':24000, 'Duration':'55days', 'Discount':1800}
    # df2 = df.append(new_row, ignore_index=True)

    print(feature)
    # print("\n")