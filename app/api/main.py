from fastapi import FastAPI
from app.api.controller import pilote_controller


app = FastAPI(
    title= "Api formule 1 projet info groupe 12",
)

app.include_router(pilote_controller.router)
