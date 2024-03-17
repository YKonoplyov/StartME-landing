from typing import List
from datetime import datetime

from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, or_, and_
# from sqlalchemy.exc import 

import schemas
import models
from utils.exceptions import ObjectNotFound

async def get_found_list(db: AsyncSession) -> List[models.Found]:
    list_query = select(models.Found).options(selectinload(models.Found.managers))
    founds_list = await db.scalars(list_query)
    return founds_list

async def get_found_by_id(db: AsyncSession, found_id: int) -> models.Found:
    found_query = select(models.Found).where(models.Found.id == found_id)
    found = await db.scalar(found_query)
    if not found:
        raise ObjectNotFound
    return found

async def update_found_by_id(db: AsyncSession, found_id: int, found_new_data: schemas.FoundUpdate) -> models.Found:
    update_query = update(models.Found).where(models.Found.id == found_id).values(found_new_data.create_update_dict())
    await db.execute(update_query)
    await db.commit()
    updated_found = await get_found_by_id(db=db, found_id=found_id)
    return updated_found

async def create_found(db: AsyncSession, found_data: schemas.FoundCreate) -> models.Found:
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

async def found_add_manager(found_id: int, user_id: int, db: AsyncSession) -> None:
    found = await db.scalar(select(models.Found).where(models.Found.id == found_id).options(selectinload(models.Found.managers)))
    new_manager = await db.scalar(select(models.User).where(models.User.role.in_([models.Roles.ADMIN, models.Roles.MANAGER]), models.User.id == user_id))
    try:
        found.managers.append(new_manager)
        await db.commit()
    except Exception as e:
        await db.rollback()


async def get_records_list(db: AsyncSession, search_query: str, found_id: int) -> List[models.Record]:
    records_query = select(models.Record).options(
        selectinload(models.Record.user),
        selectinload(models.Record.found),
        selectinload(models.Record.previous_versions)
    ).order_by(models.Record.created_at.desc())
    
    if found_id:
        records_query = records_query.where(
            models.Record.found_id == found_id
        )
    
    if search_query:
        records_query = records_query.where(
            or_(
                models.Record.user.has(models.User.username.ilike(f"%{search_query}%")),
                models.Record.user.has(models.User.email.ilike(f"%{search_query}%")),
                models.Record.arbitrage.ilike(f"%{search_query}%"),
                models.Record.comment.ilike(f"%{search_query}%")
            )
        )

    records = await db.execute(records_query)
    return records.scalars().all()

async def get_record_by_id(db: AsyncSession, record_id: int) -> models.Record:
    record_by_id_query = select(models.Record).where(models.Record.id == record_id).options(
        selectinload(models.Record.user),
        selectinload(models.Record.found),
        selectinload(models.Record.previous_versions)
    )
    record = await db.execute(record_by_id_query)
    db_record = record.scalars().first()
    if db_record is None:
        # Handle the case where the record with the given ID doesn't exist
        raise ObjectNotFound
    return db_record


async def create_record(db: AsyncSession, record_data: schemas.RecordCreate):
    create_record_query = insert(models.Record).values(**record_data.create_update_dict())
    try:
        created_record_data = await db.execute(create_record_query)
        await db.commit()
        new_record = await get_record_by_id(
            record_id=created_record_data.inserted_primary_key[0],
            db=db    
        )
        print(new_record)
        return new_record
    except Exception as e:

        await db.rollback()
        print(e)

async def update_record_by_id(db: AsyncSession, record_id: int, new_data: schemas.RecordCreate) -> models.Record:
    record = await get_record_by_id(record_id=record_id, db=db)
    
    previous_version = models.RecordHistory(
        user_id=record.user_id,
        found_id=record.found_id,
        created_at=record.created_at,
        updated_at=record.updated_at,
        arbitrage=record.arbitrage,
        comment=record.comment,
        current_version=record.id
    )

    update_data = new_data.create_update_dict()
    update_data["updated_at"] = datetime.now()
    
    for key, value in update_data.items():
        setattr(record, key, value)

    record.previous_versions.append(previous_version)

    await db.commit()

    await db.refresh(record)

    return record

async def  delete_record_by_id(db: AsyncSession, record_id: int) -> None:
    record_to_delete = await get_record_by_id(db=db, record_id=record_id)

    