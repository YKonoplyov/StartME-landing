from typing import List
from datetime import datetime

from sqlalchemy.orm import selectinload, lazyload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, or_, and_

# from sqlalchemy.exc import

import schemas
import models
from utils.exceptions import ObjectNotFound, Forbidden
from users import UserManager


async def get_found_list(db: AsyncSession) -> List[models.Found]:
    list_query = select(models.Found).options(selectinload(models.Found.managers))
    founds_list = await db.scalars(list_query)
    return founds_list


async def get_found_by_id(db: AsyncSession, found_id: int, current_user: models.User = None) -> models.Found:
    found_query = select(models.Found).where(models.Found.id == found_id).options(
        selectinload(models.Found.managers),
        selectinload(models.Found.owner)
        )
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
    user_manager: UserManager,
    current_user: models.User = None,
) -> models.Found:
    found_to_update = await get_found_by_id(found_id=found_id, db=db, current_user=current_user)
    update_data = found_new_data.create_update_dict()
    try:
        owner_id = update_data.pop("owner_id")
    except:
        owner_id =  None
    for key, value in update_data.items():
        setattr(found_to_update, key, value)
    if owner_id:
        found_to_update.owner = await user_manager.get(owner_id)
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
            selectinload(models.Record.nicknames),
            selectinload(models.Record.previous_versions).options(selectinload(models.RecordHistory.nicknames)),
            selectinload(models.Record.created_by),
            selectinload(models.Record.found),
        )
        .order_by(models.Record.created_at.desc())
    )

    if found_id:
        records_query = records_query.where(models.Record.found_id == found_id)

    if search_query:
        records_query = records_query.where(
            or_(
                models.Record.description.ilike(f"%{search_query}%"),
                models.Record.first_name.ilike(f"%{search_query}%"),
                models.Record.last_name.ilike(f"%{search_query}%"),
                models.Record.middlename.ilike(f"%{search_query}%"),
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
            selectinload(models.Record.nicknames),
            selectinload(models.Record.previous_versions).options(selectinload(models.RecordHistory.nicknames)),
            selectinload(models.Record.created_by),
            selectinload(models.Record.found),
        )
    )
    record = await db.scalar(record_by_id_query)

    if record is None:
        raise ObjectNotFound
    print(record.__dict__)
    return record



async def create_record(db: AsyncSession, record_data: schemas.RecordCreate):
    record_data = record_data.model_dump()
    nicknames = record_data.pop("nicknames")
    found = await get_found_by_id(db=db, found_id=record_data.pop("fund_id"))
    create_record_query = insert(models.Record).values(
        record_data
    )

    
    try:
        created_record_data = await db.execute(create_record_query)
        await db.commit()
        new_record = await get_record_by_id(
            record_id=created_record_data.inserted_primary_key[0], db=db
        )
        new_record.found = found
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
    for attr in ['first_name', 'last_name', 'middlename', 'gipsyteam', 'pokerstrategy', 'description', 'amount', 'google', 'mail', 'vk', 'facebook', 'blog', 'instagram', 'forum', 'neteller', 'skrill', 'ecopayz', 'old', 'fundName', 'nicknameOld', 'comments', 'country', 'town', 'address', 'created_by_id', 'created_at', 'webmoney_id', 'wallets', 'updated_at', 'old_id']:
        setattr(previous_version, attr, getattr(record, attr))

    # Create a copy of the list of nicknames
    nicknames_copy = list(record.nicknames)
    
    for old_nickname in nicknames_copy:
        previous_version.nicknames.append(old_nickname)

    db.add(previous_version)
    update_data = new_data.create_update_dict()
    try:
        updated_nicknames_dicts = update_data.pop("nicknames")
    except:
        updated_nicknames_dicts = None
    update_data["updated_at"] = datetime.now()
    
    for key, value in update_data.items():
        setattr(record, key, value)

    if updated_nicknames_dicts:
        record.nicknames.clear()
        updated_nicknames = [models.Nickname(**nickname_dict) for nickname_dict in updated_nicknames_dicts]
        record.nicknames.clear()
        record.nicknames.extend(updated_nicknames)
        
    record.previous_versions.append(previous_version)

    await db.commit()

    return record


async def delete_record_by_id(db: AsyncSession, record_id: int) -> None:
    record_to_delete = await get_record_by_id(db=db, record_id=record_id)
