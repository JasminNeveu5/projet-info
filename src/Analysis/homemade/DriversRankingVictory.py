from options.config import DATA_DIR
from src.Common.utils import merge, read_csv
from src.Model.Driver import Driver


def count_driver_ids(list_of_dicos):
    driver_id_counts = {}

    for dico in list_of_dicos:
        driver_id = dico.get("driverId")
        if driver_id:
            if driver_id in driver_id_counts:
                driver_id_counts[driver_id] += 1
            else:
                driver_id_counts[driver_id] = 1
    result = [
        {"driverId": driver_id, "nb_victoires": count}
        for driver_id, count in driver_id_counts.items()
    ]
    return result


def get_winners(results: list):
    winners = []
    for dico in results:
        if dico["position"] == "1":
            winners.append(dico)

    return winners


def get_ranking_victory(nb_victory: int):
    if not isinstance(nb_victory, int):
        raise TypeError("nb_victory doit être de type int")
    if nb_victory < 0:
        raise ValueError("nb_victory doit être positif")

    drivers_path = f"{DATA_DIR}/drivers.csv"
    results_path = f"{DATA_DIR}/results.csv"
    drivers = read_csv(drivers_path)
    results = read_csv(results_path)
    winners = get_winners(results)
    winners_victoires = count_driver_ids(winners)
    winners_victoires_name = []
    for dico in winners_victoires:
        if dico["nb_victoires"] > 50:
            winners_victoires_name.append(dico)

    full = merge(winners_victoires_name, drivers, "driverId")
    liste_retour = []
    for ligne in full:
        liste_retour.append(
            Driver(
                id=int(ligne["driverId"]),
                forename=ligne["forename"],
                surname=ligne["surname"],
                nationality=ligne["nationality"],
                nombre_victoire=ligne["nb_victoires"],
            )
        )
    return liste_retour
