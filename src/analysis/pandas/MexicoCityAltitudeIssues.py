from options.config import DATA_DIR
import pandas as pd


# Fonction


def MexicoCityAltitudeIssue(wanted_status):
    results = pd.read_csv(f"{DATA_DIR}/results.csv")
    races = pd.read_csv(f"{DATA_DIR}/races.csv")
    circuits = pd.read_csv(f"{DATA_DIR}/circuits.csv")
    status = pd.read_csv(f"{DATA_DIR}/status.csv")

    jointure = pd.merge(results, status, on="statusId", how="left")
    jointure = pd.merge(jointure, races, on="raceId", how="left")
    jointure = pd.merge(jointure, circuits, on="circuitId", how="left")
    jointure = jointure[["location", "status"]][jointure["status"] == wanted_status]

    moyenne = (
        jointure[jointure["status"] == wanted_status]
        .groupby("location")
        .value_counts()
        .mean()
    )
    nombre_mexico = (
        jointure[
            (jointure["status"] == wanted_status)
            & (jointure["location"] == "Mexico City")
        ]
        .groupby("location")
        .value_counts()[0]
    )
    return float(moyenne), float(nombre_mexico)


print(MexicoCityAltitudeIssue("Engine"))
