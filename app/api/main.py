from fastapi import FastAPI
from api.controller import pilote_controller


app = FastAPI()

app.include_router(pilote_controller.router)
