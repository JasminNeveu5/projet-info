import pytest
from src.model.internal.driver import Driver
from src.analysis.pandas.DriversByNationality import DriversByNationality

# test with the available data on
# https://fr.wikipedia.org/wiki/Championnat_du_monde_de_Formule_1_2022#Classements_saison_2022

"""
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

"""
@pytest.mark.parametrize(
    "wanted_nationality, expected_results",
    [
        (
            "Czech"
            [
                Driver(gngn)
            ],
        )
    ],
)
def testDriversByNatinality(wanted_nationality, expected_results):
    assert(DriversByNationality(wanted_nationality) == expected_results)