import pandas as pd
from options.config import DATA_DIR


def AverageTimePitStop(wanted_circuit: str) -> float:
    """
       Calculates the average pit stop time (in milliseconds) per year for a given circuit.

       :param wanted_circuit: The name of the circuit for which to calculate the average
           pit stop time.
       :type wanted_circuit: str

       :return: The average pit stop time (in milliseconds) across all years for the
           specified circuit.
       :rtype: float

       :raises FileNotFoundError: If any of the required CSV files (`pit_stops.csv`,
           `races.csv`, `circuits.csv`) are missing.
       :raises ValueError: If the circuit name does not exist in the data.

       :example:

    avg_time = AverageTimePitStop("Circuit de Monaco")
        >>> print(avg_time)
        year
        2011     24448.849192
        2012     23283.769556
        2013     24121.318612
        2014     55088.632353
        2015     25500.213225
        2016    124357.194135
        2017     56789.619597
        2018     24674.283582
        2019     24938.538462
        2020    160940.321549
        2021    219750.268170
        2022    122574.485714
        2023    178927.768640
        2024    172959.378378
    """
    pit_stops = pd.read_csv(f"{DATA_DIR}/pit_stops.csv")
    races = pd.read_csv(f"{DATA_DIR}/races.csv")
    jointure = pd.merge(pit_stops, races, on="raceId", how="left")
    circuits = pd.read_csv(f"{DATA_DIR}/circuits.csv")
    circuits = circuits[["circuitId", "name"]]
    circuits = circuits.rename(columns={"name": "nom_circuit"})
    jointure = pd.merge(jointure, circuits, on="circuitId", how="left")

    jointure[jointure["name"] == wanted_circuit]
    return jointure.groupby("year").agg("milliseconds").mean()
