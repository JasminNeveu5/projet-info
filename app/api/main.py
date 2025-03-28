from fastapi import FastAPI
from app.api.controller import pilote_controller


app = FastAPI()

app.include_router(pilote_controller.router)
