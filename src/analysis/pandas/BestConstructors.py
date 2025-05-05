import pandas as pd
from options.config import DATA_DIR
from src.model.internal.constructor import Constructor


def BestConstructors(wanted_year: str):
    """
       Returns a list of constructors with their total points for a given year.

       This function reads data from CSV files containing constructor results, constructor
       information, and race data. It filters the results by the specified year, aggregates
       the total points earned by each constructor, and returns a list of `Constructor`
       objects containing the name, nationality, and total points (interpreted as wins).

       :param wanted_year: The year for which to retrieve the best constructors.
       :type wanted_year: int

       :return: A list of Constructor objects representing the best constructors in the
           given year, sorted by total points.
       :rtype: list[Constructor]

       :raises FileNotFoundError: If any of the required CSV files are missing.
       :raises ValueError: If no constructor data is available for the specified year.
       :raises IndexError: If a constructor's nationality cannot be matched from the
           constructors data.

       :example:

    top_constructors = BestConstructors(2022)
        >>> for constructor in top_constructors:
        ...     print(constructor)
        Name: Red Bull
        Country: Austrian
        wins: 759.0
        Name: Ferrari
        Country: Italian
        wins: 554.0
        Name: Mercedes
        Country: German
        wins: 515.0
        Name: Alpine F1 Team
        Country: French
        wins: 173.0
        Name: McLaren
        Country: British
        wins: 159.0
        Name: Alfa Romeo
        Country: Swiss
        wins: 55.0
        Name: Aston Martin
        Country: British
        wins: 55.0
        Name: Haas F1 Team
        Country: American
        wins: 37.0
        Name: AlphaTauri
        Country: Italian
        wins: 35.0
        Name: Williams
        Country: British
        wins: 8.0
    """
    if not isinstance(wanted_year, int):
        raise TypeError("A year has to be a integer.")
    elif wanted_year > 2024 or wanted_year < 1950:
        raise ValueError("The available data is between 1950 and 2024.")
    else:
        constructor_results = pd.read_csv(f"{DATA_DIR}/constructor_results.csv")
        constructors = pd.read_csv(f"{DATA_DIR}/constructors.csv")
        races = pd.read_csv(f"{DATA_DIR}/races.csv")

        merged_df = pd.merge(constructor_results, races, on="raceId")
        merged_df = pd.merge(merged_df, constructors, on="constructorId")
        filtered_df = merged_df[merged_df["year"] == wanted_year]

        constructor_points = (
            filtered_df.groupby("name_y")["points"]
            .sum()
            .reset_index(name="total_points")
        )
        BestConstructorList = []
        for index, row in constructor_points.iterrows():
            constructor_nationality = constructors.loc[
                constructors["name"] == row["name_y"], "nationality"
            ].values[0]
            BestConstructorList.append(
                Constructor(
                    name=row["name_y"],
                    nationality=constructor_nationality,
                    wins=row["total_points"],
                )
            )
        BestConstructorList.sort(
            key=lambda c: c.additional_info.get("wins", 0), reverse=True
        )
        return BestConstructorList


if __name__ == "__main__":
    for truc in BestConstructors(2022):
        print(type(truc))