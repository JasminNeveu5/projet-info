import pandas as pd
from options.config import DATA_DIR


pit_stops = pd.read_csv(f'{DATA_DIR}/pit_stops.csv')
races = pd.read_csv(f'{DATA_DIR}/races.csv')

jointure = pd.merge(pit_stops, races, on='raceId', how='left')

name = 'Australian Grand Prix'

temps_moyen_pit_stops = jointure[jointure['name'] == name].groupby('year')['milliseconds'].mean()
temps_moyen_pit_stops
