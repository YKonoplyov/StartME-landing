from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, Depends, HTTPException, Response, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users.router import common
from fastapi_users import exceptions as users_exceptions
from fastapi_users import models as fast_users_models
from fastapi_users.authentication import Strategy
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
import crud
import schemas
import routers
import permissions
from db.users_db import User
from db.engine import get_async_session
from users import auth_backend, fastapi_users, UserManager, get_user_manager
from utils.exceptions import ObjectNotfund, Forbidden, NotEnoughPermissions


disable_installed_extensions_check()

app = FastAPI(root_path="/api/v1")

origins = [
    "http://nginx",
    "https://nginx"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get(
    "/funds",
    response_model=Page[schemas.FundRead],
    tags=["funds"],
    dependencies=[Depends(permissions.manager_or_higher)],
)
async def get_funds_list(db: AsyncSession = Depends(get_async_session)):
    funds_list = await crud.get_fund_list(db=db)
    return paginate(list(funds_list))


@app.get(
    "/funds/{fund_id}",
    response_model=schemas.FundRead,
    tags=["funds"],
    dependencies=[Depends(permissions.manager_or_higher)],
)
async def get_fund_by_id(
    fund_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(permissions.manager_or_higher)
    ):
    try:
        fund = await crud.get_fund_by_id(
            db=db, 
            fund_id=fund_id, 
        )
    except ObjectNotfund:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Object not fund"
        )
    except Forbidden:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return fund


@app.post(
    "/funds",
    response_model=schemas.FundRead,
    tags=["funds"],
    dependencies=[Depends(permissions.manager_or_higher)],
)
async def create_fund(
    fund_data: schemas.FundCreate, db: AsyncSession = Depends(get_async_session)
):
    new_fund = await crud.create_fund(db=db, fund_data=fund_data)
    return new_fund


@app.patch(
    "/funds/{fund_id}",
    response_model=schemas.FundRead,
    tags=["funds"]
)
async def update_fund_by_id(
    fund_id: int,
    fund_data: schemas.FundUpdate,
    db: AsyncSession = Depends(get_async_session),
    user_manager: UserManager = Depends(get_user_manager),
    current_user: User = Depends(permissions.manager_or_higher)
):
    try:
        updated_fund = await crud.update_fund_by_id(
            db=db, 
            fund_id=fund_id, 
            fund_new_data=fund_data,
            user_manager=user_manager,
            current_user=current_user
        )
    except ObjectNotfund:
        raise HTTPException(status_code=400, detail="No such fund")
    return updated_fund


@app.delete(
    "/funds/{fund_id}",
    tags=["funds"],
    dependencies=[Depends(permissions.manager_or_higher)],
)
async def delete_fund_by_id(
    fund_id: int, db: AsyncSession = Depends(get_async_session)
):
    try:
        await crud.delete_fund_by_id(db=db, fund_id=fund_id)
    except ObjectNotfund:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No such fund")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post(
    "/funds/add_manager",
    tags=["funds"],
    dependencies=[Depends(permissions.manager_or_higher)],
)
async def add_manager(
    fund_id: int, manager_id: int, db: AsyncSession = Depends(get_async_session)
):
    try:
        await crud.fund_add_manager(fund_id=fund_id, user_id=manager_id, db=db)
    except ObjectNotfund:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already assigned"
        )
    return Response(status_code=status.HTTP_200_OK)

@app.post(
        "/auth/jwt/refresh",
        name=f"auth:{auth_backend.name}.refresh",
        tags=["auth"]
    )
async def refresh(
    refresh_token: str, # TODO: changer refresh token transport
    refresh_strategy: Strategy[fast_users_models.UP, fast_users_models.ID] = Depends(auth_backend.get_refresh_strategy),
    strategy: Strategy[fast_users_models.UP, fast_users_models.ID] = Depends(auth_backend.get_strategy),
    user_manager: UserManager = Depends(get_user_manager)
):
    user = await refresh_strategy.read_token(refresh_token, user_manager)
    response = await auth_backend.login(strategy, user)
    return response

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
    # current_user = Depends(permissions.read_only_or_higher)
):
    try:
        created_user = await user_manager.create_with_funds(
            user_create, safe=True, request=request, 
            # current_user=current_user
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
    except NotEnoughPermissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return created_user

app.include_router(
    routers.get_users_router(
        user_schema=schemas.UserRead,
        user_update_schema=schemas.UserUpdate,
        get_user_manager=get_user_manager,
        authenticator=fastapi_users.authenticator
    ),
    prefix="/users",
    tags=["users"],
)


@app.get(
    "/records",
    response_model=Page[schemas.RecordRead],
    tags=["records"],
    dependencies=[Depends(permissions.read_only_or_higher)],
)
async def get_records_list(
    search_query: str | None = None,
    fund_id: int | None = None,
    db: AsyncSession = Depends(get_async_session),
):
    records_list = await crud.get_records_list(
        search_query=search_query, fund_id=fund_id, db=db
    )
    return paginate(list(records_list))


@app.get(
    "/records/{record_id}",
    response_model=schemas.RecordRead,
    tags=["records"],
    dependencies=[Depends(permissions.read_only_or_higher)],
)
async def get_record_by_id(
    record_id: int, db: AsyncSession = Depends(get_async_session)
):
    try:
        record = await crud.get_record_by_id(db=db, record_id=record_id)
    except ObjectNotfund:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return record


@app.post(
    "/records",
    response_model=schemas.RecordRead,
    tags=["records"],
    dependencies=[Depends(permissions.manager_or_higher)],
)
async def create_record(
    record_data: schemas.RecordCreate, db: AsyncSession = Depends(get_async_session)
):
    try:
        new_record = await crud.create_record(db=db, record_data=record_data)
    except ObjectNotfund:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return new_record


@app.patch(
    "/records/{record_id}",
    response_model=schemas.RecordRead,
    tags=["records"],
    dependencies=[Depends(permissions.user_or_higher)],
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
    except ObjectNotfund:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return updated_record


@app.delete(
    "/records/{record_id}",
    tags=["records"],
    dependencies=[Depends(permissions.manager_or_higher)],
)
async def delete_record_by_id(
    record_id: int, db: AsyncSession = Depends(get_async_session)
):
    try:
        await crud.delete_record_by_id(db=db, record_id=record_id)
    except ObjectNotfund:
        raise HTTPException(status_code=400, detail="No such record")
    return Response(status_code=204)


add_pagination(app)
