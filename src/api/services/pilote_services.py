import pandas as pd
from options.config import DATA_DIR
from src.analysis.pandas.DriversRankingVictory import get_ranking_victory
from src.analysis.pandas.driverRankingYear import get_ranking_year
from src.analysis.pandas.BestConstructors import BestConstructors
from src.analysis.pandas.BestTimeCircuit import get_bestTimeCircuit
from src.analysis.pandas.HomeWin import home_win
from src.analysis.pandas.MostDamagedDriver import most_damaged_driver
from src.analysis.pandas.TightestRace import tightestrace
from src.analysis.pandas.FrequentProblemsInCar import get_status_code_occurrences
from src.api.services.converter_services import ConverterService
from src.model.internal.race import Race


class DefaultQuery:
    @staticmethod
    def nombre_victoires(nb_victoires):
        drivers = get_ranking_victory(nb_victoires)
        drivers = [ConverterService.convert_to_driverAPI(driver) for driver in drivers]
        return drivers

    @staticmethod
    def rankingYear(annee: int):
        drivers = get_ranking_year(annee)
        drivers = [ConverterService.convert_to_driverAPI(driver) for driver in drivers]
        return drivers

    @staticmethod
    def bestConstructor(annee: int):
        constructors = BestConstructors(annee)
        constructors = [
            ConverterService.convert_to_constructorAPI(constructor)
            for constructor in constructors
        ]
        return constructors

    @staticmethod
    def bestTimeCircuit(name: str):
        circuit = get_bestTimeCircuit(name)
        circuit = ConverterService.convert_to_circuitAPI(circuit)
        return circuit

    @staticmethod
    def home_win(nationalite: str):
        drivers = home_win(nationalite)
        drivers = [ConverterService.convert_to_driverAPI(driver) for driver in drivers]
        return drivers

    @staticmethod
    def mostDamagedDriver(nombre_courses_minimum):
        drivers = most_damaged_driver(nombre_courses_minimum)
        drivers = [ConverterService.convert_to_driverAPI(driver) for driver in drivers]
        return drivers

    @staticmethod
    def tightestRace():
        race = tightestrace()
        r = ConverterService.convert_to_raceAPI(race)
        return r

    @staticmethod
    def get_status_code_occurences(status: str, manufacturer: str):
        constructors = get_status_code_occurrences(status, manufacturer)
        constructors = [
            ConverterService.convert_to_constructorAPI(constructor)
            for constructor in constructors
        ]
        return constructors
