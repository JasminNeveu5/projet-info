from fastapi import HTTPException, APIRouter
from api.services.pilote_services import DefaultQuery

router = APIRouter()


@router.get("/q1_{nb_victoires}")
async def q1(nb_victoires: int):
    if nb_victoires < 0:
        raise HTTPException(status_code=404,
                            detail="Nombre de victoire Invalide")
    return DefaultQuery.q1(nb_victoires)
