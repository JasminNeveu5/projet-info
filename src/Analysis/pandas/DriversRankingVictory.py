import pandas as pd
from options.config import DATA_DIR
from src.Model.Driver import Driver


def get_ranking_victory(nb_victory: int) -> list[Driver]:
    if not isinstance(nb_victory, int):
        raise TypeError("nb_victory doit être de type int")
    if nb_victory <0:
        raise ValueError("nb_victory doit être positif")

    results = pd.read_csv(f"{DATA_DIR}/results.csv")
    drivers = pd.read_csv(f"{DATA_DIR}/drivers.csv")
    winners = results[results["position"] == "1"]
    winners_victoires = (
        winners.groupby("driverId").size().reset_index(name="Nombre de victoires")
    )
    winners_victoires_name = pd.merge(winners_victoires, drivers, on="driverId")[
        ["forename", "surname", "nationality", "Nombre de victoires"]
    ].sort_values(by="Nombre de victoires", ascending=False)
    winners_victoires_name[winners_victoires_name["Nombre de victoires"] >= nb_victory]

    result = []

    for index, row in winners_victoires_name.iterrows():
        result.append(
            Driver(
                id=index,
                forename=row["forename"],
                surname=row["surname"],
                nationality=row["nationality"],
                nombre_victoire=row["Nombre de victoires"],
            )
        )
    return result
