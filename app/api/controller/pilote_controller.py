from fastapi import HTTPException, APIRouter
from app.api.services.pilote_services import DefaultQuery
import pandas as pd
from options.config import DATA_DIR
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
