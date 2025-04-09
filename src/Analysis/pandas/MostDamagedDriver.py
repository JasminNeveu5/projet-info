from src.Model.Driver import Driver
import pandas as pd
from options.config import DATA_DIR


def most_damaged_driver(nombre_courses_minimum = 0):
    if not isinstance(nombre_courses_minimum, int):
        raise TypeError("nombre_courses_minimum doit être de type int")

    results = pd.read_csv(f"{DATA_DIR}/results.csv")
    drivers = pd.read_csv(f"{DATA_DIR}/drivers.csv")

    results_accident = results.query("statusId == 3").groupby("driverId").agg(nombre_accident = ("statusId","sum")).sort_values("nombre_accident", ascending=False).merge(drivers,on = "driverId")[["driverId","forename","surname","nationality","nombre_accident"]]


    results_total = results.groupby("driverId").size().reset_index(name="count")
    results_total = pd.merge(results_total, results_accident, on="driverId")

    results_total["ratio"] = 100*results_total["nombre_accident"] / results_total["count"]
    results_total = results_total.sort_values("ratio", ascending=False)
    results_total = results_total[results_total["count"]>= nombre_courses_minimum]
    result = []

    for index, row in results_total.iterrows():
        result.append(
            Driver(
                id=row["driverId"],
                forename=row["forename"],
                surname=row["surname"],
                nationality=row["nationality"],
                nombre_accidents = row["nombre_accident"],
                nombre_courses = row["count"],
                ratio = row["ratio"]

            )
        )
    return result

print(most_damaged_driver(300)[0])
