import pandas as pd
#from src.Common.utils import convert_to_human_readable, human_readable_formatter
#import matplotlib.pyplot as plt
#from matplotlib.ticker import FuncFormatter


# Import et création de la table utilisée



pit_stops = pd.read_csv(f"{DATA_DIR}/pit_stops.csv")
races = pd.read_csv(f"{DATA_DIR}/races.csv")
jointure = pd.merge(pit_stops, races, on="raceId", how="left")


def temps_moyen_pit_stops(circuit: str) -> float:
    return jointure.groupby('year')['milliseconds'][circuit].mean()


# Graphique


name = 'Australian Grand Prix'
temps_moyen_pit_stops_readable = AverageTimePitStop(name).map(convert_to_human_readable)


plt.figure(figsize=(10, 6))
AverageTimePitStop(name).plot(
    x='year',
    y='milliseconds',
    marker="o",
    ylim=(0, 1000000),
    color='orange'
)
plt.gca().yaxis.set_major_formatter(FuncFormatter(human_readable_formatter))
plt.title(f'Temps passé au pit-stops au {name} par année', fontsize=16)
plt.xlabel("Année", fontsize=14)
plt.ylabel("Temps du pit-stops", fontsize=14)
plt.tight_layout()
plt.show()
