from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, HTTPException, Response, status, Request
from fastapi.middleware.cors import CORSMiddleware

import permissions
import crud
import schemas
from db.users_db import User
from db.engine import get_async_session
from users import auth_backend, fastapi_users, UserManager, get_user_manager
from fastapi_users.router import common
from fastapi_users import exceptions as users_exceptions
from fastapi_users import models as fast_users_models

from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.utils import disable_installed_extensions_check

from utils.exceptions import ObjectNotFound, Forbidden

disable_installed_extensions_check()

app = FastAPI(root_path="/api/v1")




@app.get(
    "/founds",
    response_model=Page[schemas.FoundRead],
    tags=["founds"],
    # dependencies=[Depends(permissions.manager_or_higher)],
)
async def get_founds_list(db: AsyncSession = Depends(get_async_session)):
    founds_list = await crud.get_found_list(db=db)
    return paginate(list(founds_list))


@app.get(
    "/founds/{found_id}",
    response_model=schemas.FoundRead,
    tags=["founds"],
    # dependencies=[Depends(permissions.manager_or_higher)],
)
async def get_found_by_id(
    found_id: int,
    db: AsyncSession = Depends(get_async_session),
    # current_user: User = Depends(permissions.manager_or_higher)
    ):
    try:
        found = await crud.get_found_by_id(
            db=db, 
            found_id=found_id, 
            # current_user=current_user
        )
    except ObjectNotFound:
        raise HTTPException(code=400, detail="No such found")
    except Forbidden:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return found


@app.post(
    "/founds",
    response_model=schemas.FoundRead,
    tags=["founds"],
    # dependencies=[Depends(permissions.manager_or_higher)],
)
async def create_found(
    found_data: schemas.FoundCreate, db: AsyncSession = Depends(get_async_session)
):
    new_found = await crud.create_found(db=db, found_data=found_data)
    return new_found


@app.patch(
    "/founds/{found_id}",
    response_model=schemas.FoundRead,
    tags=["founds"]
)
async def update_found_by_id(
    found_id: int,
    found_data: schemas.FoundUpdate,
    db: AsyncSession = Depends(get_async_session),
    # current_user: User = Depends(permissions.manager_or_higher)
):
    try:
        updated_found = await crud.update_found_by_id(
            db=db, 
            found_id=found_id, 
            found_new_data=found_data, 
            # current_user=current_user
        )
    except ObjectNotFound:
        return HTTPException(status_code=400, detail="No such found")
    return updated_found


@app.delete(
    "/founds/{found_id}",
    tags=["founds"],
    # dependencies=[Depends(permissions.manager_or_higher)],
)
async def delete_found_by_id(
    found_id: int, db: AsyncSession = Depends(get_async_session)
):
    try:
        await crud.delete_found_by_id(db=db, found_id=found_id)
    except ObjectNotFound:
        return HTTPException(status_code=400, detail="No such found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post(
    "/founds/add_manager",
    tags=["founds"],
    # dependencies=[Depends(permissions.manager_or_higher)],
)
async def add_manager(
    found_id: int, manager_id: int, db: AsyncSession = Depends(get_async_session)
):
    await crud.found_add_manager(found_id=found_id, user_id=manager_id, db=db)
    return


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)


@app.post(
    "/register",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
    name="register:register",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": common.ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        common.ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                            "summary": "A user with this email already exists.",
                            "value": {
                                "detail": common.ErrorCode.REGISTER_USER_ALREADY_EXISTS
                            },
                        },
                        common.ErrorCode.REGISTER_INVALID_PASSWORD: {
                            "summary": "Password validation failed.",
                            "value": {
                                "detail": {
                                    "code": common.ErrorCode.REGISTER_INVALID_PASSWORD,
                                    "reason": "Password should be"
                                    "at least 3 characters",
                                }
                            },
                        },
                    }
                }
            },
        },
    },
    tags=["auth"],
)
async def register(
    request: Request,
    user_create: schemas.UserCreate,  # type: ignore
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        created_user = await user_manager.create_with_founds(
            user_create, safe=True, request=request
        )
    except users_exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=common.ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )
    except users_exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": common.ErrorCode.REGISTER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    return created_user


app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(schemas.UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(schemas.UserRead, schemas.UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get(
    "/users",
    tags=["users"],
    # dependencies=[Depends(permissions.manager_or_higher)],
    response_model=Page[schemas.UserRead],
)
async def get_users_list(user_manager: UserManager = Depends(get_user_manager)):
    return paginate(list(await user_manager.get_all_users()))


@app.get(
    "/records",
    response_model=Page[schemas.RecordRead],
    tags=["records"],
    # dependencies=[Depends(permissions.read_only_or_higher)],
)
async def get_records_list(
    search_query: str | None = None,
    found_id: int | None = None,
    db: AsyncSession = Depends(get_async_session),
):
    records_list = await crud.get_records_list(
        search_query=search_query, found_id=found_id, db=db
    )
    return paginate(list(records_list))


@app.get(
    "/records/{record_id}",
    response_model=schemas.RecordRead,
    tags=["records"],
    # dependencies=[Depends(permissions.read_only_or_higher)],
)
async def get_record_by_id(
    record_id: int, db: AsyncSession = Depends(get_async_session)
):
    try:
        record = await crud.get_record_by_id(db=db, record_id=record_id)
    except ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return record


@app.post(
    "/records",
    response_model=schemas.RecordRead,
    tags=["records"],
    # dependencies=[Depends(permissions.manager_or_higher)],
)
async def create_record(
    record_data: schemas.RecordCreate, db: AsyncSession = Depends(get_async_session)
):
    try:
        new_record = await crud.create_record(db=db, record_data=record_data)
    except ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return new_record


@app.patch(
    "/records/{record_id}",
    response_model=schemas.RecordRead,
    tags=["records"],
    # dependencies=[Depends(permissions.manager_or_higher)],
)
async def update_record_by_id(
    record_id: int,
    record_data: schemas.RecordUpdate,
    db: AsyncSession = Depends(get_async_session),
) -> schemas.RecordRead:
    try:    
        updated_record = await crud.update_record_by_id(
            record_id=record_id, new_data=record_data, db=db
        )
    except ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return updated_record


@app.delete(
    "/records/{record_id}",
    tags=["records"],
    # dependencies=[Depends(permissions.manager_or_higher)],
)
async def delete_record_by_id(
    record_id: int, db: AsyncSession = Depends(get_async_session)
):
    try:
        await crud.delete_record_by_id(db=db, record_id=record_id)
    except ObjectNotFound:
        raise HTTPException(status_code=400, detail="No such record")
    return Response(status_code=204)


add_pagination(app)
