from src.model.internal.driver import Driver
from src.model.api.driver import Driver as DriverAPI
from src.model.internal.race import Race
from src.model.api.race import Race as RaceAPI
from src.model.internal.circuit import Circuit
from src.model.api.circuit import Circuit as CircuitAPI
from src.model.internal.constructor import Constructor
from src.model.api.constructor import Constructor as ConstructorAPI

class ConverterService:
    @staticmethod
    def convert_to_driverAPI(custom_driver: Driver) -> DriverAPI:
        driver_data = {
            "forename": custom_driver.forename,
            "surname": custom_driver.surname,  # Note: matches your Pydantic model's field name
            "nationality": custom_driver.nationality
        }

        if hasattr(custom_driver, 'additional_info') and custom_driver.additional_info:
            driver_data.update(custom_driver.additional_info)
        return DriverAPI(**driver_data)

    @staticmethod
    def convert_to_raceAPI(race: Race):
        race_data = {
            "name": race.name,
            "year": race.year,
            "date": race.date
        }
        if hasattr(race, 'additional_info') and race.additional_info:
            race_data.update(race.additional_info)
        return RaceAPI(**race_data)

    @staticmethod
    def convert_to_circuitAPI(circuit: Circuit):
        circuit_data = {
            "name": circuit.name,
            "location": circuit.location,
            "country": circuit.country
        }
        if hasattr(circuit, 'additional_info') and circuit.additional_info:
            circuit_data.update(circuit.additional_info)
        return CircuitAPI(**circuit_data)

    @staticmethod
    def convert_to_constructorAPI(constructor: Constructor):
        constructor_data = {
            "name": constructor.name,
            "nationality": constructor.nationality
        }
        if hasattr(constructor, 'additional_info') and constructor.additional_info:
            constructor_data.update(constructor.additional_info)
        return ConstructorAPI(**constructor_data)
