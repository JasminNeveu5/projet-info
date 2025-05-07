from fastapi import HTTPException, APIRouter, Path
import pandas as pd
from src.api.services.pilote_services import DefaultQuery
from options.config import DATA_DIR

router = APIRouter()

@router.get("/nombre_victoire_{nb_victoires}")
async def nombre_victoire(
    nb_victoires: int = Path(..., description="Minimum number of victories (e.g., 5)")
):
    if nb_victoires < 0:
        raise HTTPException(status_code=404, detail="Invalid number of victories")
    return DefaultQuery.nombre_victoires(nb_victoires)


@router.get("/classement_annee_{annee}")
async def classement_annee(
    annee: int = Path(..., description="Season year to retrieve the ranking for (1950–2024)")
):
    if annee > 2024 or annee < 1950:
        raise HTTPException(status_code=404, detail="Invalid year")
    return DefaultQuery.rankingYear(annee)


@router.get("/meilleurs_constructeurs_{annee}")
async def meilleurs_constructeurs(
    annee: int = Path(..., description="Season year to retrieve top-performing constructors (1950–2024)")
):
    if annee > 2024 or annee < 1950:
        raise HTTPException(status_code=404, detail="Invalid year")
    return DefaultQuery.bestConstructor(annee)


@router.get("/meilleur_temps_circuit_{name}")
async def meilleur_temps_circuit(
    name: str = Path(..., description="Exact name of the circuit (e.g., Circuit de Monaco)")
):
    circuit = pd.read_csv(f"{DATA_DIR}/circuits.csv")
    if name not in circuit["name"].values:
        raise HTTPException(status_code=404, detail="Invalid circuit name (e.g., Circuit de Monaco)")
    return DefaultQuery.bestTimeCircuit(name)


@router.get("/home_win_{nationalite}")
async def home_win(
    nationalite: str = Path(..., description="Driver nationality in lowercase (e.g., french)")
):
    drivers = pd.read_csv(f"{DATA_DIR}/drivers.csv")
    if nationalite not in drivers["nationality"].str.lower().values:
        raise HTTPException(status_code=404, detail="Invalid nationality (e.g., french)")
    return DefaultQuery.home_win(nationalite)


@router.get("/pilotes_accidents_{nombre_courses_minimum}")
async def pilotes_accidents(
    nombre_courses_minimum: int = Path(..., description="Minimum number of races completed by the driver (e.g., 20)")
):
    if nombre_courses_minimum < 0:
        raise HTTPException(status_code=404, detail="Invalid number of races")
    return DefaultQuery.mostDamagedDriver(nombre_courses_minimum)


@router.get("/course_plus_serree")
async def course_plus_serree():
    return DefaultQuery.tightestRace()


@router.get("/probleme_constructeur_{status}/{manufacturer}")
async def probleme_constructeur(
    status: str = Path(..., description="Type of issue or retirement (e.g., Engine, Brakes, Accident...)"),
    manufacturer: str = Path(..., description="Constructor name in lowercase (e.g., ferrari)")
):
    constructors = pd.read_csv(f"{DATA_DIR}/constructors.csv")
    if manufacturer not in constructors["name"].str.lower().values:
        raise HTTPException(status_code=404, detail="Invalid constructor (e.g., ferrari)")
    return DefaultQuery.get_status_code_occurences(status, manufacturer)
