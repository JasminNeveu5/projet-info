import pandas as pd
from options.config import DATA_DIR
from src.model.internal.driver import Driver


def DriversByNationality(wanted_nationality:str):
    """
    Retrieves a list of Driver objects that match the specified nationality.

    This function reads the drivers data from a CSV file, filters it by the given nationality,
    and returns a list of Driver objects containing forename, surname, and nationality.

    :param wanted_nationality: The nationality to filter drivers by.
    :type wanted_nationality: str

    :return: A list of Driver objects with the specified nationality.
    :rtype: list[Driver]

    :raises FileNotFoundError: If the drivers CSV file is not found.
    :raises ValueError: If no drivers match the given nationality.

    :example:

    australian_drivers = DriversByNationality("Australian")
     >>> for driver in australian_drivers:
     ...     print(driver.forename, driver.surname)
     Mark Webber
     David Brabham
     Gary Brabham
     Alan Jones
     Larry Perkins
     Brian McGuire
     Vern Schuppan
     Warwick Brown
     Tim Schenken
     David Walker
     Jack Brabham
     Frank Gardner
     Paul Hawkins
     Ken Kavanagh
     Paul England
     Tony Gaze
     Daniel Ricciardo
     Oscar Piastri
    """
    drivers = pd.read_csv(f"{DATA_DIR}/drivers.csv")
    df = drivers[drivers['nationality'] == wanted_nationality]
    driversList = []
    for index, row in df.iterrows():
        driversList.append(
                Driver(
                    forename=row["forename"],
                    surname=row["surname"],
                    nationality=row['nationality']
                )
            )
    return driversList
    
if __name__ == "__main__":
    # Example usage
    australian_drivers = DriversByNationality("Australian")
    for driver in australian_drivers:
        print(driver.forename, driver.surname)
    print(DriversByNationality("Czech")[0].forename)