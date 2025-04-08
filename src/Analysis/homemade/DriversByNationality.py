import csv
from options.config import DATA_DIR
import matplotlib.pyplot as plt
import numpy as np


def DriversByNationality(wanted_nationality):
    with open(f'{DATA_DIR}/drivers.csv', encoding='utf-8', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        drivers_list = []
        nb_line = 0
        for row in reader:
            nb_line += 1
            if row['nationality'] == wanted_nationality:
                drivers_list.append(f'{row['forename']} {row['surname']}')
    nationality_proportion = len(drivers_list)/nb_line
    return nationality_proportion, drivers_list


# Exemple pris

wanted_nationality = 'Italian'


# Graphique

nationality_proportion = DriversByNationality(wanted_nationality)[0]
y = np.array([nationality_proportion, 1 - nationality_proportion])
mylabels = [f"{wanted_nationality}", "Other nationalities"]
myexplode = [0.2, 0]
mycolors = ['yellow', 'lightblue']

plt.pie(
        y,
        labels=mylabels,
        explode=myexplode,
        colors=mycolors,
        autopct='%1.1f%%'
)
plt.title(f'Part of {wanted_nationality} among drivers')
plt.show()
