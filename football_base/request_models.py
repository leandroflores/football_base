from pydantic import BaseModel

class League(BaseModel):
    name: str
    season: str
    details: str
    country: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()
