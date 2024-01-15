import pandas as pd
import json
import matplotlib.pyplot as plt
import prophet as pr
from datetime import datetime, timedelta

""" UTILS FUNCTIONS """
def extract_date(s):
    # s is a string in json format
    # Extract ['features'][0]['properties']['mdate'] from the JSON data
    data = json.loads(s)
    mdate = data['features'][0]['properties']['mdate']
    
    # Convert to datetime format
    dt_with_timezone = datetime.fromisoformat(mdate)
    
    # Convert to a naive datetime object (remove timezone information)
    dt_naive = dt_with_timezone.replace(tzinfo=None)
    
    return dt_naive

""" SETTINGS """
DIRECTORY = "data/"
DATASET = "dataset.json"
DECONNECTEE_VALUE = "DECONNECTEE"

""" PARSE """
# Initialiser une liste pour stocker les données
data_list = []
data_list_per_day = []
data_list_prophet = []

""" PROPHET INSTANCE"""
prophet_instance = pr.Prophet()

with open(DIRECTORY + DATASET, "r") as read_file:
    # Lire chaque ligne du fichier
    for line in read_file:
        if line == "\n":
            continue
        # Charger la ligne JSON
        data = json.loads(line)

        # Utiliser extract_date pour obtenir la date
        mdate = extract_date(line)

        feature = data['features'][0]

        # Extraire les champs nécessaires
        nbplaces = feature['properties']['nbplaces']
        nbvelos = feature['properties']['nbvelos']
        nbelec = feature['properties']['nbelec']
        nbclassiq = feature['properties']['nbclassiq']
        etat = feature['properties']['etat']

        # Calculer le pourcentage d'occupation
        occupation_percentage = 1 - nbplaces / (nbplaces + nbvelos)

        # Ajouter les données à la liste principale
        data_list.append({'mdate': mdate, 'y': occupation_percentage, 'etat': etat})
        data_list_prophet.append({'ds': mdate, 'y': occupation_percentage})
        
        # Convertir la date en format de jour uniquement
        day_only = mdate.replace(minute=0, second=0)

        # Ajouter les données à la liste par jour
        data_list_per_day.append({'ds': day_only, 'y': occupation_percentage, 'etat': etat})
        

# Créer un DataFrame Pandas à partir de la liste principale
df = pd.DataFrame(data_list)
df_prophet = pd.DataFrame(data_list_prophet)
#prophet_instance.fit(df)
# Convertir la colonne 'mdate' en format de date
df['mdate'] = pd.to_datetime(df['mdate'])
df_prophet['ds'] = pd.to_datetime(df['mdate'])

# Trier le DataFrame par date
df = df.loc[df['mdate'].apply(lambda x: x not in [pd.NaT])]
df_prophet = df_prophet.loc[df_prophet['ds'].apply(lambda x: x not in [pd.NaT])]
df = df.sort_values(by='mdate')
df_prophet = df_prophet.sort_values(by='ds')

future = pd.DataFrame() 
future['ds'] = df_prophet['ds']#.apply(lambda x: (x + pd.DateOffset(years=1)).date())
future = future.drop_duplicates()
future = future.iloc[0:10000]

model = pr.Prophet()
model.fit(df_prophet)
forecast = model.predict(future) 
#print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())

# Créer un DataFrame Pandas pour les données par jour
df_per_day = pd.DataFrame(data_list_per_day)
# Afficher le nombre de journées uniques
num_unique_days = df_per_day['ds'].nunique()
print("Number of unique hours:", num_unique_days)
aggregation_funtion = {'ds': 'first', 'y': 'mean', 'etat': 'first'}
df_per_day = df_per_day.groupby('ds').aggregate(aggregation_funtion)
df_per_day = df_per_day.iloc[:2000]
# Tacer les points avec etat=="DECONNECTEE" en rouge et les autres en bleu
plt.figure(figsize=(10, 6))

# Plotting points with etat=="DECONNECTEE" in red (case-insensitive) and smaller points
# plt.scatter(df[df['etat'].str.lower() == DECONNECTEE_VALUE.lower()]['mdate'], df[df['etat'].str.lower() == DECONNECTEE_VALUE.lower()]['y'], c='red', label=DECONNECTEE_VALUE, s=40)

# Plotting other points in blue and smaller points
# plt.scatter(df_per_day[df_per_day['etat'].str.lower() != DECONNECTEE_VALUE.lower()]['ds'], df_per_day[df_per_day['etat'].str.lower() != DECONNECTEE_VALUE.lower()]['y'], c='blue', label='Occupation Percentage', s=4)
# plt.scatter(df[df['etat'].str.lower() != DECONNECTEE_VALUE.lower()]['mdate'], df[df['etat'].str.lower() != DECONNECTEE_VALUE.lower()]['y'], c='blue', label='Occupation Percentage', s=4)

# Connecting all points with a line
plt.plot(df_per_day['ds'], df_per_day['y'], color='black', linestyle='-', linewidth=0.5)
# plt.plot(df['mdate'], df['y'], color='black', linestyle='-', linewidth=1)

# Prophet plot
plt.plot(forecast['ds'], forecast['yhat'], color="green", linestyle='-', linewidth=1)
plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='green', alpha = 0.1)

plt.title('Occupation Percentage Over Time')
plt.xlabel('Date and Time')
plt.ylabel('Occupation Percentage')
plt.legend()
plt.show()
