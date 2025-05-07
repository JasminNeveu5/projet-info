import pytest
from src.model.internal.driver import Driver
from src.analysis.pandas.DriversByNationality import DriversByNationality

# test with the available data on
# https://en.wikipedia.org/wiki/List_of_Formula_One_drivers


@pytest.mark.parametrize(
    "param, typeerror, error",
    [
        (2022, TypeError, "The nationality must be a str."),
        (9.0, TypeError, "The nationality must be a str."),
    ],
)
def testParamTypes(param, typeerror, error):
    with pytest.raises(typeerror, match=error):
        DriversByNationality(param)


@pytest.mark.parametrize(
    "wanted_nationality, expected_results",
    [
        (
            "Malaysian",
            [
                Driver("Alex", "Yoong", "Malaysian")
            ]
        ),
        (
            "Venezuelan",
            [
                Driver("Johnny", "Cecotto", "Venezuelan"),
                Driver("Ettore", "Chimeri", "Venezuelan"),
                Driver("Pastor", "Maldonado", "Venezuelan")
            ]
        ),
    ],
)
def testDriversByNatinality(wanted_nationality, expected_results):
    assert (DriversByNationality(wanted_nationality) == expected_results)
