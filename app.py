from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, HTTPException, Response, status, Request
import permissions
import crud
import schemas
from db.users_db import User
from db.engine import get_async_session
from users import auth_backend, fastapi_users, UserManager, get_user_manager
from fastapi_users.router import common
from fastapi_users import exceptions
from fastapi_users import models as fast_users_models


app = FastAPI()

@app.get("/founds", response_model=List[schemas.FoundRead], dependencies=[Depends(permissions.manager_or_higher)])
async def get_founds_list(db: AsyncSession = Depends(get_async_session)):
    founds_list = await crud.get_found_list(db=db)
    return founds_list

@app.get("/founds/{found_id}", response_model=schemas.FoundRead)
async def get_found_by_id(found_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        found = await crud.get_found_by_id(db=db, found_id=found_id)
    except:
        return HTTPException(
            code=400, detail="No such found"
        )
    return found

@app.post("/founds", response_model=schemas.FoundRead)
async def create_found(
    found_data: schemas.FoundCreate,
    db: AsyncSession = Depends(get_async_session)
):
    new_found = await crud.create_found(db=db, found_data=found_data)
    return new_found

@app.patch("/founds/{found_id}", response_model=schemas.FoundRead,)
async def update_found_by_id(
    found_id: int,
    found_data: schemas.FoundUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        updated_found = await crud.update_found_by_id(db=db, found_id=found_id, found_new_data=found_data)
    except:
        return HTTPException(
            code=400, detail="No such found"
        )
    return updated_found

@app.delete("/founds/{found_id}")
async def delete_found_by_id(found_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        await crud.delete_found_by_id(db=db, found_id=found_id)
    except:
        return HTTPException(
            code=400, detail="No such found"
        )
    return Response(status_code=204)

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
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=common.ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )
    except exceptions.InvalidPasswordException as e:
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
