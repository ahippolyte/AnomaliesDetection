import pandas as pd
import json
import matplotlib.pyplot as plt

""" SETTINGS """
DIRECTORY = "data/"
DATASET = "dataset.json"
DECONNECTEE_VALUE = "DECONNECTEE"

""" PARSE """
# Initialiser une liste pour stocker les données
data_list = []

with open(DIRECTORY + DATASET, "r") as read_file:
    # Lire chaque ligne du fichier
    for line in read_file:
        if line == "\n":
            continue
        # Charger la ligne JSON
        data = json.loads(line)
        feature = data['features'][0]

        # Extraire les champs nécessaires
        mdate = feature['properties']['mdate']
        nbplaces = feature['properties']['nbplaces']
        nbvelos = feature['properties']['nbvelos']
        nbelec = feature['properties']['nbelec']
        nbclassiq = feature['properties']['nbclassiq']
        etat = feature['properties']['etat']

        # Calculer le pourcentage d'occupation
        occupation_percentage = 1 - nbplaces / (nbplaces + nbvelos)

        # Ajouter les données à la liste
        data_list.append({'mdate': mdate, 'occupation_percentage': occupation_percentage, 'etat': etat})

# Créer un DataFrame Pandas à partir de la liste de données
df = pd.DataFrame(data_list)

# Convertir la colonne 'mdate' en format de date
df['mdate'] = pd.to_datetime(df['mdate'])

# Trier le DataFrame par date
df = df.sort_values(by='mdate')

# Tacer les points avec etat=="DECONNECTEE" en rouge et les autres en bleu
plt.figure(figsize=(10, 6))

# Plotting points with etat=="DECONNECTEE" in red (case-insensitive) and smaller points
plt.scatter(df[df['etat'].str.lower() == DECONNECTEE_VALUE.lower()]['mdate'], df[df['etat'].str.lower() == DECONNECTEE_VALUE.lower()]['occupation_percentage'], c='red', label=DECONNECTEE_VALUE, s=40)

# Plotting other points in blue and smaller points
plt.scatter(df[df['etat'].str.lower() != DECONNECTEE_VALUE.lower()]['mdate'], df[df['etat'].str.lower() != DECONNECTEE_VALUE.lower()]['occupation_percentage'], c='blue', label='Occupation Percentage', s=4)

# Connecting all points with a line
plt.plot(df['mdate'], df['occupation_percentage'], color='black', linestyle='-', linewidth=0.5)

plt.title('Occupation Percentage Over Time')
plt.xlabel('Date and Time')
plt.ylabel('Occupation Percentage')
plt.legend()
plt.show()
