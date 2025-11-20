# /models/species_model.py

from sqlalchemy import Column, Integer, String, Text
from .base import BaseModel # 🚨 models/base.py에서 BaseModel 임포트

class Species(BaseModel):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True, index=True)
    name_kr = Column(String(255), index=True, nullable=False)
    name_en = Column(String(255), index=True)
    description = Column(Text)