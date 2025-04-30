from pydantic import BaseModel


class Driver(BaseModel):
    forename: str
    surname: str  # Consider renaming to 'surname' to match your custom class
    nationality: str

    class Config:
        extra = "allow"  # This allows additional fields beyond those defined
