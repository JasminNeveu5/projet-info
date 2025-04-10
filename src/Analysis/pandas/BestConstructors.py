import pandas as pd
import numpy as np
from options.config import DATA_DIR
import matplotlib.pyplot as plt


constructor_standings = pd.read_csv(f'{DATA_DIR}/constructor_standings.csv')
constructors = pd.read_csv(f'{DATA_DIR}/constructors.csv')
races = pd.read_csv(f'{DATA_DIR}/races.csv')

jointure = pd.merge(constructor_standings, constructors, on='constructorId', how='left')
jointure = pd.merge(jointure, races, on='raceId', how='left')
jointure = jointure[['name_x', 'year', 'wins']]


# Fonction


def BestConstructors(wanted_year):
    result = jointure[jointure['year'] == wanted_year].groupby('name_x').apply(np.sum, axis=0).sort_values('wins', ascending=False) # agg({'wins':sum}))
    result['name'] = result.index
    return result


# Exemple pris


wanted_year = 2003


# Graphique


BestConstructors(wanted_year).plot.bar(
    x='name',
    y='wins',
    color='darkmagenta'
)
plt.title(f'Nombre de victoires par constructeur en {wanted_year}', fontsize=20)
plt.xlabel("Constructeurs", fontsize=14)
plt.ylabel("Nombre de victoires", fontsize=14)
plt.tight_layout()
plt.show()
