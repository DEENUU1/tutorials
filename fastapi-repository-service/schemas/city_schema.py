from pydantic import BaseModel, UUID4, Field
from .region_schema import RegionOutput


class CityInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    region_id: UUID4


class CityInDb(BaseModel):
    id: UUID4
    name: str
    region_id: UUID4

    class Config:
        orm_mode = True


class CityOutput(BaseModel):
    id: UUID4
    name: str
    region: RegionOutput