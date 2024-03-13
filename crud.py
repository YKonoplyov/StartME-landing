from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
import schemas
import models

async def get_found_list(db: AsyncSession) -> List[models.Found]:
    list_query = select(models.Found)
    founds_list = await db.scalars(list_query)
    return founds_list

async def get_found_by_id(db: AsyncSession, found_id: int) -> models.Found:
    found_query = select(models.Found).where(models.Found.id == found_id)
    found = await db.scalar(found_query)
    return found

async def create_found(db: AsyncSession, found_data: schemas.FoundCreate) -> models:
    creation_query = insert(models.Found).values(found_data.model_dump())
    new_found_result = await db.execute(creation_query)
    await db.commit()
    new_found = await get_found_by_id(
        db=db, found_id=new_found_result.inserted_primary_key[0]
    )
    return new_found

async def delete_found_by_id(db: AsyncSession, found_id: int) -> None:
    found_to_delete = await get_found_by_id(db=db, found_id=found_id)
    await db.delete(found_to_delete)
    await db.commit()
    
    return
    