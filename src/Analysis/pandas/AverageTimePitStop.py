import pandas as pd

# from src.Common.utils import convert_to_human_readable, human_readable_formatter
# import matplotlib.pyplot as plt
# from matplotlib.ticker import FuncFormatter


# Code


pit_stops = pd.read_csv("C:/DEVOIRS/ENSAI1A/projet-info/data/pit_stops.csv")
races = pd.read_csv("C:/DEVOIRS/ENSAI1A/projet-info/data/races.csv")
jointure = pd.merge(pit_stops, races, on="raceId", how="left")


def temps_moyen_pit_stops(circuit: str) -> float:
    return jointure.groupby("year")["milliseconds"][circuit].mean()


# Graphique
"""
temps_moyen_pit_stops_readable = temps_moyen_pit_stops.map(convert_to_human_readable)
temps_moyen_pit_stops_readable


plt.figure(figsize=(10, 6))
plt.axhline(y=60000, color='gray', linestyle='--')
plt.axhline(y=120000, color='gray', linestyle='--')
plt.axhline(y=180000, color='gray', linestyle='--')
plt.text(2011, 60000, '1min', backgroundcolor='lightgrey')
plt.text(2011, 120000, '2min', backgroundcolor='lightgrey')
plt.text(2011, 180000, '3min', backgroundcolor='lightgrey')
temps_moyen_pit_stops().plot(
    x='year',
    y='milliseconds',
    marker="o",
    ylim=(0, 230000),
    color='orange'
)
plt.gca().yaxis.set_major_formatter(FuncFormatter(human_readable_formatter))
plt.title('Temps passé au pit-stops par année', fontsize=16)
plt.xlabel("Année", fontsize=14)
plt.ylabel("Temps du pit-stops", fontsize=14)
plt.tight_layout()
"""
