from options.config import DATA_DIR
import pandas as pd
import warnings


# Fonction
def MexicoCityAltitudeIssue(wanted_status_name:str):
    # Suppress warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        results = pd.read_csv(f"{DATA_DIR}/results.csv")
        races = pd.read_csv(f"{DATA_DIR}/races.csv")
        circuits = pd.read_csv(f"{DATA_DIR}/circuits.csv")
        status = pd.read_csv(f"{DATA_DIR}/status.csv")

        jointure = pd.merge(results, status, on="statusId", how="left")
        jointure = pd.merge(jointure, races, on="raceId", how="left")
        jointure = pd.merge(jointure, circuits, on="circuitId", how="left")
        jointure = jointure[["location", "status"]][jointure["status"] == wanted_status_name]

        moyenne = (
            jointure[jointure["status"] == wanted_status_name]
            .groupby("location")
            .value_counts()
            .mean()
        )
        nombre_mexico = (
            jointure[
                (jointure["status"] == wanted_status_name)
                & (jointure["location"] == "Mexico City")
            ]
            .groupby("location")
            .value_counts()[0]
        )
        # moyenne is the average number of problem on all circuits, 
        # and nombre_mexico is the number of problem on Mexico City
        # On average, mexico city has more problems than the average of all circuits
        # due to its altitude.
        return float(moyenne), float(nombre_mexico)

if __name__ == "__main__":
    print(MexicoCityAltitudeIssue("Engine"))
