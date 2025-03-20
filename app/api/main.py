import pandas as pd
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    return {"hello": "world"}


@app.get("/q1_{nb_victoires}")
async def q1(nb_victoires: int):
    results = pd.read_csv("~/Documents/1A-ENSAI/projet-info/data/results.csv")
    drivers = pd.read_csv("~/Documents/1A-ENSAI/projet-info/data/drivers.csv")
    return (
        pd.merge(results, drivers, on="driverId")
        .query("position == '1'")
        .groupby(["driverId", "forename", "surname"])
        .size()
        .reset_index(name="Victoires")
        .query(f"Victoires >= {nb_victoires}")
        .sort_values("Victoires", ascending=False)
        .to_json(orient="records")
    )


@app.get("/q2_{annee}")
async def q2(annee: int):
    results = pd.read_csv("~/Documents/1A-ENSAI/projet-info/data/results.csv")
    drivers = pd.read_csv("~/Documents/1A-ENSAI/projet-info/data/drivers.csv")
    races = pd.read_csv("~/Documents/1A-ENSAI/projet-info/data/races.csv")
    return pd.merge(
        pd.merge(results, races[races["year"] == annee], on="raceId")
        .groupby("driverId")
        .sum("points")
        .sort_values("points", ascending=False),
        drivers,
        on="driverId",
    )[["forename", "surname", "points"]].to_json(orient="records")
