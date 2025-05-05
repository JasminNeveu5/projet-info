import pytest
from src.model.internal.constructor import Constructor
from src.analysis.pandas.BestConstructors import BestConstructors

# test with the available data on
# https://fr.wikipedia.org/wiki/Championnat_du_monde_de_Formule_1_2022#Classements_saison_2022


@pytest.mark.parametrize(
    "param, typeerror, error",
    [
        ("2022", TypeError, "A year has to be a integer."),
        (2022.9, TypeError, "A year has to be a integer."),
        (2025, ValueError, "The available data is between 1950 and 2024."),
    ],
)
def testParamTypes(param, typeerror, error):
    with pytest.raises(typeerror, match=error):
        BestConstructors(param)

@pytest.mark.parametrize(
    "wanted_year, expected_results",
    [
        (
            2022,
            [
                Constructor("Red Bull", "Austrian", wins=759.0),
                Constructor("Ferrari", "Italian", wins=554.0),
                Constructor("Mercedes", "German", wins=515.0),
                Constructor("Alpine F1 Team", "French", wins=173.0),
                Constructor("McLaren", "British", wins=159.0),
                Constructor("Alfa Romeo", "Swiss", wins=55.0),
                Constructor("Aston Martin", "British", wins=55.0),
                Constructor("Haas F1 Team", "American", wins=37.0),
                Constructor("AlphaTauri", "Italian", wins=35.0),
                Constructor("Williams", "British", wins=8.0),
            ],
        )
    ],
)
def testBestConstructorsRanking(wanted_year, expected_results):
    actual = BestConstructors(wanted_year)
    assert len(actual) == len(expected_results)
    for a, e in zip(actual, expected_results):
        assert a.name == e.name
        assert a.nationality == e.nationality
        assert a.additional_info == e.additional_info

@pytest.mark.parametrize(
    "wanted_year, expected_names",
    [
        (2022, [
            "Red Bull", "Ferrari", "Mercedes", "Alpine F1 Team", "McLaren",
            "Alfa Romeo", "Aston Martin", "Haas F1 Team", "AlphaTauri", "Williams"
        ]),
    ],
)
def testBestConstructorsNames(wanted_year, expected_names):
    actual = BestConstructors(wanted_year)
    actual_names = [c.name for c in actual]
    assert actual_names == expected_names

@pytest.mark.parametrize(
    "wanted_year, expected_nationalities",
    [
        (2022, [
            "Austrian", "Italian", "German", "French", "British",
            "Swiss", "British", "American", "Italian", "British"
        ]),
    ],
)
def testBestConstructorsNationalities(wanted_year, expected_nationalities):
    actual = BestConstructors(wanted_year)
    actual_nationalities = [c.nationality for c in actual]
    assert actual_nationalities == expected_nationalities

@pytest.mark.parametrize(
    "wanted_year, expected_wins",
    [
        (2022, [
            759.0, 554.0, 515.0, 173.0, 159.0, 55.0, 55.0, 37.0, 35.0, 8.0
        ]),
    ],
)
def testBestConstructorsWins(wanted_year, expected_wins):
    actual = BestConstructors(wanted_year)
    actual_wins = [c.additional_info.get("wins") for c in actual]
    assert actual_wins == expected_wins