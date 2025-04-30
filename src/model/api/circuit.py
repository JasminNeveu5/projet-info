from pydantic import BaseModel


class Circuit(BaseModel):
    name: str
    location: str
    country: str

    class Config:
        extra = "allow"
