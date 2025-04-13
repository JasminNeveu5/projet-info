from options.config import DATA_DIR
import pandas as pd
results = pd.read_csv(f"{DATA_DIR}/results.csv")
races = pd.read_csv(f"{DATA_DIR}/races.csv")
drivers = pd.read_csv(f"{DATA_DIR}/drivers.csv")
constructor_standings = pd.read_csv(f"{DATA_DIR}/constructor_standings.csv")
qualifying = pd.read_csv(f"{DATA_DIR}/qualifying.csv")
lap_times = pd.read_csv(f"{DATA_DIR}/lap_times.csv")
weather = pd.read_csv(f"{DATA_DIR}/weather.csv")

class Pretraitement:
    # renvoie le jeu de données final
    @staticmethod
    def prepare():
        df = pd.DataFrame()

        df["driver_name"] = drivers["forename"] + " " + drivers["surname"]
        df["driverId"] = drivers["driverId"]
        df = df.merge(results, on="driverId")
        df = df.merge(races, on="raceId")
        df["race_name"] = df["name"]

        # ajout des performances des courses précedentes
        df.sort_values("date", ascending=True, inplace=True)
        df["perf_n1"] = df.groupby("driverId")["positionOrder"].shift(1)
        df["perf_n2"] = df.groupby("driverId")["positionOrder"].shift(2)
        df["perf_n3"] = df.groupby("driverId")["positionOrder"].shift(3)

        # Vitesse moyenne sur circuit
        df["avg_lap_time"] = df.groupby(["driverId","race_name"])
        return df[df["driver_name"] == "Lewis Hamilton"][["driver_name", "race_name","avg_lap_time"]]



print(Pretraitement.prepare())
