from fastapi import FastAPI
from services.pilote_services import DefaultQuery


app = FastAPI()


@app.get("/")
async def index():
    return {"hello": "autre"}


@app.get("/q1_{nb_victoires}")
async def q1(nb_victoires: int):
    return DefaultQuery.q1(nb_victoires)


@app.get("/q2_{annee}")
async def q2(annee: int):
    return DefaultQuery.q2(annee)
