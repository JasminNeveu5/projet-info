import pandas as pd
from options.config import DATA_DIR
from src.Common.utils import convert_to_human_readable, human_readable_formatter
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt


# Import et création de la table utilisée

pit_stops = pd.read_csv(f"{DATA_DIR}/pit_stops.csv")
races = pd.read_csv(f"{DATA_DIR}/races.csv")
jointure = pd.merge(pit_stops, races, on="raceId", how="left")
circuits = pd.read_csv(f"{DATA_DIR}/circuits.csv")
circuits = circuits[['circuitId', 'name']]
circuits = circuits.rename(columns={'name': 'nom_circuit'})
jointure = pd.merge(jointure, circuits, on="circuitId", how="left")


# Fonction

# à faire : filtrer par circuit
def AverageTimePitStop(circuit_demande: str) -> float:
    return jointure.groupby('year').agg('milliseconds').mean()


# Exemple pris


name = 'Australian Grand Prix'


# Graphique


temps_moyen_pit_stops_readable = AverageTimePitStop(name).map(convert_to_human_readable)
plt.figure(figsize=(10, 6))
AverageTimePitStop(name).plot(
    x='year',
    y='milliseconds',
    marker="o",
    ylim=(0, 240000),
    color='orange'
)
plt.gca().yaxis.set_major_formatter(FuncFormatter(human_readable_formatter))
plt.title(f'Temps passé au pit-stops au {name} par année', fontsize=16)
plt.xlabel("Année", fontsize=14)
plt.ylabel("Temps du pit-stops", fontsize=14)
plt.tight_layout()
plt.show()
