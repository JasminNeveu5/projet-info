from fastapi import HTTPException, APIRouter
import pandas as pd
from src.api.services.pilote_services import DefaultQuery
from options.config import DATA_DIR

router = APIRouter()


@router.get("/nombre_victoire_{nb_victoires}")
async def nombre_victoire(nb_victoires: int):
    if nb_victoires < 0:
        raise HTTPException(status_code=404, detail="Nombre de victoire Invalide")
    return DefaultQuery.nombre_victoires(nb_victoires)


@router.get("/classement_annee_{annee}")
async def classement_annee(annee: int):
    if annee > 2024 or annee <= 1950:
        raise HTTPException(status_code=404, detail="Annee invalide")
    return DefaultQuery.rankingYear(annee)


@router.get("/meilleurs_constructeurs_{annee}")
async def meilleurs_constructeurs(annee: int):
    if annee > 2024 or annee <= 1950:
        raise HTTPException(status_code=404, detail="Annee invalide")
    return DefaultQuery.bestConstructor(annee)


@router.get("/meilleur_temps_circuit_{name}")
async def meilleur_temps_circuit(name: str):
    circuit = pd.read_csv(f"{DATA_DIR}/circuits.csv")
    if not name in circuit["name"].values:
        raise HTTPException(status_code=404, detail="Circuit Invalide")
    return DefaultQuery.bestTimeCircuit(name)


@router.get("/home_win_{nationalite}")
async def home_win(nationalite: str):
    drivers = pd.read_csv(f"{DATA_DIR}/drivers.csv")
    if not nationalite in drivers["nationality"].str.lower().values:
        raise HTTPException(status_code=404, detail="Nationalite Invalide")
    return DefaultQuery.home_win(nationalite)


@router.get("/pilotes_accidents_{nombre_courses_minimum}")
async def pilotes_accidents(nombre_courses_minimum: int):
    if nombre_courses_minimum < 0:
        raise HTTPException(status_code=404, detail="Nombre de courses Invalide")
    return DefaultQuery.mostDamagedDriver(nombre_courses_minimum)


@router.get("/course_plus_serree")
async def course_plus_serree():
    return DefaultQuery.tightestRace()


@router.get("/probleme_constructeur_{status}/{manufacturer}")
async def probleme_constructeur(status: str, manufacturer: str):
    constructors = pd.read_csv(f"{DATA_DIR}/constructors.csv")
    if not manufacturer in constructors["name"].str.lower().values:
        raise HTTPException(status_code=404, detail="Constructeur Invalide")
    return DefaultQuery.get_status_code_occurences(status, manufacturer)
