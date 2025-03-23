import pandas as pd
import matplotlib.pyplot as plt

# Obtenir le temps moyen passé au pit-stops par année
pit_stops = pd.read_csv('C:/DEVOIRS/ENSAI1A/projet-info/data/pit_stops.csv')
races = pd.read_csv('C:/DEVOIRS/ENSAI1A/projet-info/data/races.csv')

jointure = pd.merge(pit_stops, races, on='raceId', how='left')

temps_moyen_pit_stops = jointure.groupby('year')['milliseconds'].mean()
print(temps_moyen_pit_stops)


# Graphique du temps moyen passé au pit-stops par année (à arranger)
jointure.plot(y='year', x='milliseconds', kind='hist')
plt.title("Temps moyen passé au pit-stops par année")
plt.xlabel('Année')
# plt.xticks(np.arange(2011, 2025))
plt.ylabel('Millisecondes')
plt.show()
