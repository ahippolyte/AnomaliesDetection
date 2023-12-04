import pandas as pd
import json
import matplotlib.pyplot as plt

""" SETTINGS """
DIRECTORY = "data/"
DATASET = "dataset.json"

""" PARSE """
# Initialiser une liste pour stocker les données
data_list = []

with open(DIRECTORY + DATASET, "r") as read_file:
    # Lire chaque ligne du fichier
    for line in read_file:
        # Charger la ligne JSON
        data = json.loads(line)
        feature = data['features'][0]

        # Extraire les champs nécessaires
        mdate = feature['properties']['mdate']
        nbplaces = feature['properties']['nbplaces']
        nbvelos = feature['properties']['nbvelos']
        nbelec = feature['properties']['nbelec']
        nbclassiq = feature['properties']['nbclassiq']

        # Calculer le pourcentage d'occupation
        occupation_percentage = 1 - nbplaces / (nbplaces + nbvelos )

        # Ajouter les données à la liste
        data_list.append({'mdate': mdate, 'occupation_percentage': occupation_percentage})

# Créer un DataFrame Pandas à partir de la liste de données
df = pd.DataFrame(data_list)

# Convertir la colonne 'mdate' en format de date
df['mdate'] = pd.to_datetime(df['mdate'])

# Trier le DataFrame par date
df = df.sort_values(by='mdate')

# Tracer la courbe d'occupation par rapport au temps
plt.figure(figsize=(10, 6))
plt.plot(df['mdate'], df['occupation_percentage'], label='Occupation Percentage')
plt.title('Occupation Percentage Over Time')
plt.xlabel('Date and Time')
plt.ylabel('Occupation Percentage')
plt.legend()
plt.show()
