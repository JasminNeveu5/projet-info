from options.config import DATA_DIR
from methodes_pures import read_csv, merge

drivers_path = f"{DATA_DIR}/drivers.csv"
results_path = f"{DATA_DIR}/results.csv"

drivers = read_csv(drivers_path)
results = read_csv(results_path)
drivers_x_results = merge(drivers, results, "driverId")
winners = []


for dico in results:
    if dico["position"] == "1":
        winners.append(dico)


def count_driver_ids(list_of_dicos):
    # Create an empty dictionary to store counts of driverId
    driver_id_counts = {}

    # Iterate through each dictionary in the list
    for dico in list_of_dicos:
        driver_id = dico.get("driverId")  # Get the value of driverId
        if driver_id:
            # Increment the count for this driverId
            if driver_id in driver_id_counts:
                driver_id_counts[driver_id] += 1
            else:
                driver_id_counts[driver_id] = 1

    # Convert the driver_id_counts dictionary into a list of dictionaries
    result = [
        {"driverId": driver_id, "nb_victoires": count}
        for driver_id, count in driver_id_counts.items()
    ]

    return result


winners_victoires = count_driver_ids(winners)

winners_victoires_name = []

for dico in winners_victoires:
    if dico["nb_victoires"] > 50:
        winners_victoires_name.append(dico)


print(merge(winners_victoires_name, drivers, "driverId"))
