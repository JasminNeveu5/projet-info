import pandas as pd
import numpy as np
from options.config import DATA_DIR
from src.Model.Constructor import Constructor


constructor_standings = pd.read_csv(f'{DATA_DIR}/constructor_standings.csv')
constructors = pd.read_csv(f'{DATA_DIR}/constructors.csv')
races = pd.read_csv(f'{DATA_DIR}/races.csv')

jointure = pd.merge(constructor_standings, constructors, on='constructorId', how='left')
jointure = pd.merge(jointure, races, on='raceId', how='left')
jointure = jointure[['name_x', 'year', 'wins', 'nationality']]


# Fonction


def BestConstructors(wanted_year):
    result = jointure[jointure['year'] == wanted_year].groupby('name_x').apply(np.sum, axis=0).sort_values('wins', ascending=False)
    result['name'] = result.index
    result = result[['name', 'nationality', 'wins']]

    BestConstructorList = []

    for index, row in result.iterrows():
        BestConstructorList.append(
            Constructor(
                name=row['name'],
                nationality=row['nationality'],
                wins=row['wins'],
            )
        )

    return BestConstructorList
