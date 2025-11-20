# /schemas/species_schema.py

from pydantic import BaseModel
from typing import Optional

class SpeciesBase(BaseModel):
    name_kr: str
    name_en: Optional[str] = None
    description: Optional[str] = None

class SpeciesCreate(SpeciesBase):
    pass

class Species(SpeciesBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True