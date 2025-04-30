from src.model.internal.driver import Driver
import pandas as pd
from options.config import DATA_DIR


def most_damaged_driver(nombre_courses_minimum):
    """
    Identifies the drivers with the highest accident ratio based on their number of accidents
    relative to their total races. The function filters drivers who have participated in at
    least a specified minimum number of races.

    :param nombre_courses_minimum: The minimum number of races a driver must have participated in
                                   to be considered in the analysis.
    :type nombre_courses_minimum: int
    :return: A list of Driver objects containing details of the most accident-prone drivers,
             filtered based on the minimum number of races. Each object includes driver ID,
             forename, surname, nationality, number of accidents, total number of races,
             and accident ratio.
    :rtype: list[Driver]
    """
    results = pd.read_csv(f"{DATA_DIR}/results.csv")
    drivers = pd.read_csv(f"{DATA_DIR}/drivers.csv")

    results_accident = (
        results.query("statusId == 3")
        .groupby("driverId")
        .agg(nombre_accident=("statusId", "sum"))
        .sort_values("nombre_accident", ascending=False)
        .merge(drivers, on="driverId")[
            ["driverId", "forename", "surname", "nationality", "nombre_accident"]
        ]
    )

    results_total = results.groupby("driverId").size().reset_index(name="count")
    results_total = pd.merge(results_total, results_accident, on="driverId")

    results_total["ratio"] = (
        100 * results_total["nombre_accident"] / results_total["count"]
    )
    results_total = results_total.sort_values("ratio", ascending=False)
    results_total = results_total[results_total["count"] >= nombre_courses_minimum]
    result = []

    for index, row in results_total.iterrows():
        result.append(
            Driver(
                forename=row["forename"],
                surname=row["surname"],
                nationality=row["nationality"],
                nombre_accidents=row["nombre_accident"],
                nombre_courses=row["count"],
                ratio=row["ratio"],
            )
        )
    return result
