import pandas as pd
import matplotlib.pyplot as plt

# Obtenir le temps moyen passé au pit-stops par année
pit_stops = pd.read_csv('C:/DEVOIRS/ENSAI1A/projet-info/data/pit_stops.csv')
races = pd.read_csv('C:/DEVOIRS/ENSAI1A/projet-info/data/races.csv')

jointure = pd.merge(pit_stops, races, on='raceId', how='left')

temps_moyen_pit_stops = jointure.groupby('year')['milliseconds'].mean()


# Graphique du temps moyen passé au pit-stops par année
plt.axhline(y=60000, color='gray', linestyle='--')
plt.axhline(y=120000, color='gray', linestyle='--')
plt.axhline(y=180000, color='gray', linestyle='--')
plt.text(2011, 60000, '1min', backgroundcolor='grey')
plt.text(2011, 120000, '2min', backgroundcolor='grey')
plt.text(2011, 180000, '3min', backgroundcolor='grey')
temps_moyen_pit_stops.plot(
    x='year',
    y='milliseconds',
    marker="o",
    title="Temps moyen passé au pit-stops par année",
    xlabel='Année',
    ylabel='Millisecondes',
    ylim=(0, 230000),
    color='orange'
)


plt.show()
