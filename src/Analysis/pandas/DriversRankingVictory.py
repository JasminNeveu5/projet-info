import pandas as pd
from options.config import DATA_DIR
from src.Model.Driver import Driver


def get_ranking_victory(nb_victory: int) -> list[Driver]:
    """
    Retrieve a list of drivers who have achieved at least the specified number of victories.

    This function reads data from CSV files containing race results and driver information
    to determine the number of victories per driver, filtering out drivers with fewer victories
    than the specified threshold. The function then collects and returns details of the drivers
    meeting or exceeding the specified victory count.

    :param nb_victory: The minimum number of victories a driver must have to be included in
        the result. Must be a positive integer.
    :type nb_victory: int
    :raises TypeError: If `nb_victory` is not of type int.
    :raises ValueError: If `nb_victory` is less than 0.
    :return: A list of `Driver` instances representing the drivers with at least the
        specified number of victories. Each driver contains details such as their name,
        nationality, and exact number of victories.
    :rtype: list[Driver]
    """
    if not isinstance(nb_victory, int):
        raise TypeError("nb_victory doit être de type int")
    if nb_victory < 0:
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
                forename=row["forename"],
                surname=row["surname"],
                nationality=row["nationality"],
                nombre_victoire=row["Nombre de victoires"],
            )
        )
    return result
