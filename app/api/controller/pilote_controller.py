from fastapi import HTTPException, APIRouter
from app.api.services.pilote_services import DefaultQuery
import pandas as pd
from options.config import DATA_DIR


router = APIRouter()


@router.get("/nombre_victoire_{nb_victoires}")
async def nombre_victoire(nb_victoires: int):
    if nb_victoires < 0:
        raise HTTPException(status_code=404, detail="Nombre de victoire Invalide")
    return DefaultQuery.nombre_victoire(nb_victoires)


@router.get("/classement_{annee}")
async def classement(annee: int):
    if annee < 1950 or annee > 2024:
        raise HTTPException(status_code=404, detail="Annee invalide")
    return DefaultQuery.classement(annee)


@router.get("/meilleur_tour_{localisation}")
async def meilleur_tour(localisation: str):
    circuits = pd.read_csv("../../data/circuits.csv")
    if not circuits["location"].isin([localisation]).any():
        raise HTTPException(status_code=404, detail="Invalide location")
    return DefaultQuery.meilleur_temps(localisation)


@router.get("/temps_moyen_pitstops_{annee}")
async def temps_moyen_pit_stops(annee: int):
    if annee < 1950 or annee > 2024:
        raise HTTPException(status_code=404, detail="Annee invalide")
    return DefaultQuery.temps_moyen_pitstops(annee)


@router.get("/casse_constructeur_{constructeur}")
async def casse_constructeur(constructeur: str):
    constructeurs = pd.read_csv(f"{DATA_DIR}/constructors.csv")
    if not constructeurs["name"].isin([constructeur]).any():
        raise HTTPException(status_code=404, detail="Constructeur invalide")
    return DefaultQuery.casse_constructeur(constructeur)


@router.get("/temps_dernier_qualif_{circuit}_{annee}")
async def temps_max_qualif(circuit: str, annee: str):
    """
    Retrieves the maximum qualifying time for a given circuit and year. This function queries the
    data from predefined circuit and race data files. If the specified circuit reference or year
    is invalid, an HTTP 404 error is raised.

    :param circuit: The reference identifier for the circuit, provided as a string. It must match
        one of the existing circuit references in the circuit data file.
    :param annee: The year of the qualifying record to retrieve, provided as a string. It must
        match one of the years in the race data file.
    :return: The maximum qualifying time for the specified circuit and year obtained from the
        data source.
    :rtype: str
    :raises HTTPException: Raised with a 404 status code if the given circuit or year is invalid.
    """
    circuits = pd.read_csv(f"{DATA_DIR}/circuits.csv")
    races = pd.read_csv(f"{DATA_DIR}/races.csv")
    if not circuits["circuitRef"].isin([circuit]).any():
        raise HTTPException(status_code=404, detail="Invalide circuit")
    if not races["year"].isin([int(annee)]).any():
        raise HTTPException(status_code=404, detail="Invalide annee")
    return DefaultQuery.temps_min_qualif_annee(circuit, annee)