# /cruds/species_crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.species_model import Species # 🚨 models 디렉토리에서 Species 모델 임포트
from schemas import species_schema as schemas

async def get_all_species(session: AsyncSession):
    result = await session.execute(
        select(Species).order_by(Species.name_kr)
    )
    return result.scalars().all()

async def create_species(session: AsyncSession, species: schemas.SpeciesCreate):
    db_species = Species(**species.model_dump())
    session.add(db_species)
    await session.commit()
    await session.refresh(db_species)
    return db_species