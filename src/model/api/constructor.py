from pydantic import BaseModel


class Constructor(BaseModel):
    name: str
    nationality: str

    class Config:
        extra = "allow"
