from typing import List
from datetime import datetime

from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, or_, and_

# from sqlalchemy.exc import

import schemas
import models
from utils.exceptions import ObjectNotFound, Forbidden


async def get_found_list(db: AsyncSession) -> List[models.Found]:
    list_query = select(models.Found).options(selectinload(models.Found.managers))
    founds_list = await db.scalars(list_query)
    return founds_list


async def get_found_by_id(db: AsyncSession, found_id: int, current_user: models.User = None) -> models.Found:
    found_query = select(models.Found).where(models.Found.id == found_id).options(selectinload(models.Found.managers))
    found = await db.scalar(found_query)
    if not found:
        raise ObjectNotFound
    # if current_user.role == models.Roles.MANAGER and current_user not in found.managers:
    #     raise Forbidden
    return found


async def update_found_by_id(
    db: AsyncSession,
    found_id: int,
    found_new_data: schemas.FoundUpdate,
    current_user: models.User = None
) -> models.Found:
    found_to_update = await get_found_by_id(found_id=found_id, db=db, current_user=current_user)
    update_data = found_new_data.create_update_dict()
    for key, value in update_data.items():
        setattr(found_to_update, key, value)
    
    await db.commit()
    await db.refresh(found_to_update)
    return found_to_update


async def create_found(
    db: AsyncSession, found_data: schemas.FoundCreate
) -> models.Found:
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
    found = await db.scalar(
        select(models.Found)
        .where(models.Found.id == found_id)
        .options(selectinload(models.Found.managers))
    )
    new_manager = await db.scalar(
        select(models.User).where(
            models.User.role.in_([models.Roles.ADMIN, models.Roles.MANAGER]),
            models.User.id == user_id,
        )
    )

    try:
        found.managers.append(new_manager)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


async def get_records_list(
    db: AsyncSession, search_query: str, found_id: int
) -> List[models.Record]:
    records_query = (
        select(models.Record)
        .options(
            selectinload(models.Record.previous_versions),
            selectinload(models.Record.created_by),
            selectinload(models.Record.nicknames),
        )
        .order_by(models.Record.created_at.desc())
    )

    if found_id:
        records_query = records_query.where(models.Record.found_id == found_id)

    if search_query:
        records_query = records_query.where(
            or_(
                models.Record.has(models.User.username.ilike(f"%{search_query}%")),
                models.Record.has(models.User.email.ilike(f"%{search_query}%")),
                models.Record.arbitrage.ilike(f"%{search_query}%"),
                models.Record.first_name.ilike(f"%{search_query}%"),
                models.Record.last_name.ilike(f"%{search_query}%"),
                models.Record.by_fathers_name.ilike(f"%{search_query}%"),
                models.Record.description.ilike(f"%{search_query}%"),
            )
        )

    records = await db.scalars(records_query)
    return records

async def get_record_by_id(db: AsyncSession, record_id: int) -> models.Record:
    record_by_id_query = (
        select(models.Record)
        .where(models.Record.id == record_id)
        .options(
            selectinload(models.Record.previous_versions),
            selectinload(models.Record.created_by),
            selectinload(models.Record.nicknames),
        )
    )
    record = await db.scalar(record_by_id_query)

    if record is None:
        raise ObjectNotFound
    return record


async def create_record(db: AsyncSession, record_data: schemas.RecordCreate):
    update_data = record_data.model_dump()
    nicknames = update_data.pop("nicknames")
    create_record_query = insert(models.Record).values(
    )

    
    try:
        created_record_data = await db.execute(create_record_query)
        await db.commit()
        new_record = await get_record_by_id(
            record_id=created_record_data.inserted_primary_key[0], db=db
        )
        if nicknames:
            print(nicknames)
            nicknames_list = [
                models.Nickname(
                    room_name=nickname_dict.get("room_name"),
                    nickname=nickname_dict.get("nickname")             
                ) 
                for nickname_dict in nicknames if nickname_dict
            ]
            new_record.nicknames.extend(nicknames_list)
            await db.commit()
            await db.refresh(new_record)
        return new_record
    except Exception as e:

        await db.rollback()
        raise(e)

    

async def update_record_by_id(
    db: AsyncSession, record_id: int, new_data: schemas.RecordCreate
) -> models.Record:
    record = await get_record_by_id(record_id=record_id, db=db)

    previous_version = models.RecordHistory()
    previous_version.__dict__.update(record.__dict__)

    previous_version.__dict__.update(record.__dict__)
    previous_version.nicknames = record.nicknames
    print(previous_version)
    await db.add(previous_version)

    await db.commit()

    update_data = new_data.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.now()
    for key, value in update_data.items():
        setattr(record, key, value)

    record.previous_versions.append(previous_version)
    await db.commit()

    return record

async def delete_record_by_id(db: AsyncSession, record_id: int) -> None:
    record_to_delete = await get_record_by_id(db=db, record_id=record_id)
