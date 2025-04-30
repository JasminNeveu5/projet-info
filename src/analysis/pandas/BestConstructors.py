import pandas as pd
import numpy as np
from options.config import DATA_DIR
from src.model.internal.constructor import Constructor


constructor_standings = pd.read_csv(f"{DATA_DIR}/constructor_standings.csv")
constructors = pd.read_csv(f"{DATA_DIR}/constructors.csv")
races = pd.read_csv(f"{DATA_DIR}/races.csv")

jointure = pd.merge(constructor_standings, constructors, on="constructorId", how="left")
jointure = pd.merge(jointure, races, on="raceId", how="left")
jointure = jointure[["name_x", "year", "wins", "nationality"]]


# Fonction


def best_constructors(wanted_year):
    """
    Returns a list of Constructor objects representing the best constructors for a given year.

    Args:
        wanted_year (int): The year for which to retrieve the best constructors.

    Returns:
        list[Constructor]: A list of Constructor objects sorted by number of wins in descending order.
    """
    # Group by constructor and sum wins, take the first nationality (they are always the same for a constructor)
    filtered = jointure[jointure["year"] == wanted_year]
    result = (
        filtered.groupby("name_x")
        .agg({"wins": "sum", "nationality": "first"})
        .sort_values("wins", ascending=False)
        .reset_index()
    )
    result = result.rename(columns={"name_x": "name"})

    best_constructor_list = []

    for _, row in result.iterrows():
        best_constructor_list.append(
            Constructor(
                name=row["name"],
                nationality=row["nationality"],
                wins=row["wins"],
            )
        )

    return best_constructor_list


if __name__ == "__main__":
    year = 2021
    best_constructors_list = best_constructors(year)
    for constructor in best_constructors_list:
        print(
            f"{constructor.name} - {constructor.nationality} - {constructor.additional_info["wins"]} wins"
        )
