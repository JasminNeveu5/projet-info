import csv
from options.config import DATA_DIR
from src.model.internal.driver import Driver


def DriversByNationality(wanted_nationality: str):
    """
    Retrieves the proportion of drivers from a specified nationality and returns a list
        of those drivers.

    :param wanted_nationality: The nationality of the drivers you want to filter.
    :type wanted_nationality: str

    :return: A tuple containing:
        - A float representing the proportion of drivers from the specified nationality
            relative to the total number of drivers.
        - A list of Driver objects representing the drivers from the specified
            nationality.
    :rtype: tuple(float, list)

    :raises TypeError: If the `wanted_nationality` parameter is not a string.
    :raises ValueError: If no drivers from the specified nationality are found.

    :example:

    proportion, drivers = DriversByNationality("German")
     >>> print(proportion)
     0.020954598370197905
     >>> print([f'{driver.forename} {driver.surname}' for driver in drivers])
     ['Mark Webber', 'David Brabham', 'Gary Brabham', 'Alan Jones', 'Larry Perkins',
     'Brian McGuire', 'Vern Schuppan', 'Warwick Brown', 'Tim Schenken', 'David Walker',
     'Jack Brabham', 'Frank Gardner', 'Paul Hawkins', 'Ken Kavanagh', 'Paul England',
     'Tony Gaze', 'Daniel Ricciardo', 'Oscar Piastri']
    """
    if not isinstance(wanted_nationality, str):
        raise TypeError("The wanted nationality should be a string.")
    else:
        with open(f"{DATA_DIR}/drivers.csv", encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            drivers_list = []
            nb_line = 0
            for row in reader:
                nb_line += 1
                if row["nationality"] == wanted_nationality:
                    driver = Driver(row["forename"], row["surname"], row["nationality"])
                    drivers_list.append(driver)
        if len(drivers_list) == 0:
            raise ValueError("There is no driver with this nationality.")
        else:
            nationality_proportion = len(drivers_list) / nb_line
            return nationality_proportion, drivers_list

if __name__ == "__main__":
    # Example usage
    try:
        proportion, drivers = DriversByNationality("German")
        print(f"Proportion: {proportion}")
        print("Drivers:")
        for driver in drivers:
            print(f"{driver.forename} {driver.surname}")
    except Exception as e:
        print(f"Error: {e}")