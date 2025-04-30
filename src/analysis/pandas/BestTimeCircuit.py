from options.config import DATA_DIR
import pandas as pd
from src.common.utils import human_readable_formatter
from src.model.internal.circuit import Circuit


def get_bestTimeCircuit(name: str):
    """Renvoie le meilleur temps de circuit pour une localisation donnée.
    Args:
        name(str): Le nom du circuit.
    Returns:
            Circuit: Un objet Circuit contenant le meilleur temps de circuit.
    """
    if not isinstance(name, str):
        raise TypeError("le nom du circuit doit être de type str")

    lap_times = pd.read_csv(f"{DATA_DIR}/lap_times.csv")
    circuits = pd.read_csv(f"{DATA_DIR}/circuits.csv")
    races = pd.read_csv(f"{DATA_DIR}/races.csv")

    meilleur_temps_course = (
        lap_times.groupby("raceId")["milliseconds"].min().reset_index()
    )
    m2 = (
        meilleur_temps_course.merge(races, on="raceId")
        .groupby("circuitId")["milliseconds"]
        .min()
        .reset_index()
        .merge(circuits, on="circuitId")
    )
    m2["meilleur_ever"] = m2["milliseconds"].apply(human_readable_formatter)
    f = m2[m2["name"].str.contains(name, case=False)]
    return Circuit(
        name=f["name"].values[0],
        country=f["country"].values[0],
        location=f["location"].values[0],
        best_time=f["meilleur_ever"].values[0],
    )
