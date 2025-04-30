from pydantic import BaseModel


class Race(BaseModel):
    name: str
    year: int
    date: str

    class Config:
        extra = "allow"
