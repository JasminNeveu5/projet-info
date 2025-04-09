import pandas as pd
from options.config import DATA_DIR
from src.Model.Driver import Driver


def get_ranking_year(year: int):
    """
    Generates a ranking of drivers for a specified year based on their performance
    in races during that year. The ranking considers overall points, number of wins,
    second places, and third places to rank drivers in descending order.

    :param year: The year for which the driver ranking is to be generated. Must be
        an integer between 1950 and 2024 inclusive.
    :type year: int
    :return: A list of Driver objects with the ranking results, where each object
        contains driver details (ID, forename, surname, nationality) and their total
        points for the specified year.
    :rtype: List[Driver]
    :raises TypeError: If the input `year` is not an integer.
    :raises ValueError: If the input `year` is outside the range [1950, 2024].
    """
    if not isinstance(year, int):
        raise TypeError("year doit être de type int")
    if year < 1950 or year > 2024:
        raise ValueError("year doit être compris entre 1950 et 2024")
    results = pd.read_csv(f"{DATA_DIR}/results.csv")
    drivers = pd.read_csv(f"{DATA_DIR}/drivers.csv")
    races = pd.read_csv(f"{DATA_DIR}/races.csv")

    races_year = pd.merge(results, races[races["year"] == year], on="raceId")
    races_year["positionOrder"] = races_year["positionOrder"].astype(int)
    points_wins = (
        races_year.groupby("driverId")
        .agg(
            points=("points", "sum"),
            wins=("positionOrder", lambda x: (x == 1).sum()),
            second_places=("positionOrder", lambda x: (x == 2).sum()),
            third_places=("positionOrder", lambda x: (x == 3).sum()),
        )
        .reset_index()
    )

    sorted_drivers = points_wins.sort_values(
        by=["points", "wins", "second_places", "third_places"],
        ascending=[False, False, False, False],
    )

    r = pd.merge(sorted_drivers, drivers, on="driverId")[
            ["driverId","forename", "surname","nationality" ,"points"]
    ]

    result = []
    for index, row in r.iterrows():
        result.append(
            Driver(
                id=row["driverId"],
                forename=row["forename"],
                surname=row["surname"],
                nationality=row["nationality"],
                nb_points=row["points"],
            )
        )
    return result
