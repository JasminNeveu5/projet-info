from options.config import DATA_DIR
from src.model.internal.driver import Driver
import pandas as pd


def home_win(nationalite):
    if not isinstance(nationalite, str):
        raise TypeError("nationalite doit être de type str")

    drivers = pd.read_csv(DATA_DIR / "drivers.csv")
    results = pd.read_csv(DATA_DIR / "results.csv")
    races = pd.read_csv(DATA_DIR / "races.csv")
    drivers["nationality"] = drivers["nationality"].apply(lambda x: x.lower())

    races["country"] = races["name"].apply(lambda x: x.split(" ")[0].lower())

    # Calcule de la position moyenne par pilote
    position_moyenne = (
        results.groupby("driverId")
        .agg(moyenne_overall=("positionOrder", "mean"))
        .sort_values("moyenne_overall")
    )
    position_moyenne_pilote = drivers.merge(
        position_moyenne, on="driverId", how="inner"
    )

    # Calcule de la position moyenne des pilotes lors des courses dans leurs pays
    local_races = races.merge(drivers, left_on="country", right_on="nationality")
    local_races_moyenne = (
        local_races.merge(results, on=["raceId", "driverId"])
        .groupby("driverId")
        .agg(moyenne_locale=("positionOrder", "mean"))
    )

    # Calcule de la position moyenne des pilotes lors des courses à l'étranger
    merged = results.merge(races, on="raceId").merge(drivers, on="driverId")
    foreign_races = merged[merged["country"] != merged["nationality"]]
    foreign_races_moyenne = foreign_races.groupby("driverId").agg(
        moyenne_etrangere=("positionOrder", "mean")
    )

    compare = pd.merge(
        local_races_moyenne, position_moyenne_pilote, on="driverId"
    ).merge(foreign_races_moyenne, on="driverId", how="left")
    compare = compare[
        [
            "driverId",
            "forename",
            "surname",
            "moyenne_overall",
            "moyenne_etrangere",
            "moyenne_locale",
            "nationality",
        ]
    ]
    compare = compare[compare["nationality"] == nationalite.lower()]
    compare = compare.sort_values("moyenne_locale", ascending=True)
    result = []
    for index, row in compare.iterrows():
        result.append(
            Driver(
                forename=row["forename"],
                surname=row["surname"],
                nationality=row["nationality"],
                moyenne_exterieure=row["moyenne_etrangere"],
                moyenne_generale=row["moyenne_overall"],
                moyenne_domicile=row["moyenne_locale"],
            )
        )
    result.append(
        Driver(
            forename="j",
            surname="s",
            nationality="French",
            moyenne_exterieure=1,
            moyenne_generale=2,
            moyenne_domicile=3,
        )
    )
    return result
