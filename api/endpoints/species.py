# /api/endpoints/species.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db_session
from cruds import species_crud as crud
from schemas import species_schema as schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.Species])
async def read_species_list(
    session: AsyncSession = Depends(get_db_session)
):
    db_species = await crud.get_all_species(session)
    return db_species