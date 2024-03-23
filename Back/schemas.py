from datetime import datetime
from typing import Any, Dict, Optional, List
from pydantic import BaseModel, ConfigDict

from fastapi_users import schemas as users_schemas

from models import Roles


def model_dump(model: BaseModel, *args, **kwargs) -> Dict[str, Any]:
    return model.model_dump(*args, **kwargs)


def model_validate(schema: BaseModel, obj: Any, *args, **kwargs) -> BaseModel:
    return schema.model_validate(obj, *args, **kwargs)


class CreateUpdateDictModel(BaseModel):
    def create_update_dict(self):
        return model_dump(
            self,
            exclude_unset=True,
            exclude={"id"},
        )

    def create_update_dict_superuser(self):
        return model_dump(self, exclude_unset=True, exclude={"id"})

    def convert_fields_to_optional(self):
        return {k: Optional[v] for k, v in self.__annotations__.items()}

class NicknameBase(CreateUpdateDictModel):
    room_name: Optional[str | None] = None
    nickname: Optional[str | None] = None
    model_config = ConfigDict(from_attributes=False)
class NicknameCreate(NicknameBase):
    ...

class NicknameRead(NicknameBase):
    ...

class UserRead(users_schemas.BaseUser):
    id: int
    username: str
    role: Roles
    email: Optional[str | None] = None
    created_at: datetime


class UserCreate(users_schemas.BaseUserCreate):
    username: str
    password: str
    role: Roles
    email: Optional[str | None] = None
    created_at: datetime


class UserUpdate(users_schemas.BaseUserUpdate):
    email: Optional[str | None] = None
    role: Roles


class FoundBase(CreateUpdateDictModel):
    name: Optional[str | None]
    discord: Optional[str | None]
    link: Optional[str | None]


class FoundCreate(FoundBase): ...


class FoundUpdate(FoundBase):
    name: Optional[str | None] = None
    discord: Optional[str | None] = None
    link: Optional[str | None] = None
    owner_id: Optional[int | None] = None


class FoundRead(FoundBase):
    id: int
    owner: Optional[UserRead | None] = None





# class UserRead(users_schemas.CreateUpdateDictModel):
#     ...


class RecordBase(CreateUpdateDictModel):
    first_name: Optional[str | None] = None
    last_name: Optional[str | None] = None
    middlename: Optional[str | None] = None
    nicknames: Optional[List[NicknameRead|None]] = None
    gipsyteam: Optional[str | None] = None
    pokerstrategy: Optional[str | None] = None
    description: Optional[str | None] = None
    amount: Optional[str | None] = None
    google: Optional[str | None] = None
    mail: Optional[str | None] = None
    vk: Optional[str | None] = None
    facebook: Optional[str | None] = None
    blog: Optional[str | None] = None
    instagram: Optional[str | None] = None
    forum: Optional[str | None] = None
    neteller: Optional[str | None] = None
    skrill: Optional[str | None] = None
    ecopayz: Optional[str | None] = None
    webmoney_id: Optional[str | None] = None
    wallets: Optional[str | None] = None
    old: Optional[bool | None] = None
    found: FoundRead
    nicknameOld: Optional[str | None] = None
    comments: Optional[str | None] = None
    country: Optional[str | None] = None
    town: Optional[str | None] = None
    address: Optional[str | None] = None
    
    model_config = ConfigDict(from_attributes=False)


class RecordCreate(RecordBase):
    fund_id: int


class RecordHistoryRead(RecordBase):
    id: int
    first_name: Optional[str | None] = None
    last_name: Optional[str | None] = None
    middlename: Optional[str | None] = None
    nicknames: Optional[List[NicknameRead|None]] = None
    gipsyteam: Optional[str | None] = None
    pokerstrategy: Optional[str | None] = None
    description: Optional[str | None] = None
    amount: Optional[str | None] = None
    google: Optional[str | None] = None
    mail: Optional[str | None] = None
    vk: Optional[str | None] = None
    facebook: Optional[str | None] = None
    blog: Optional[str | None] = None
    instagram: Optional[str | None] = None
    forum: Optional[str | None] = None
    neteller: Optional[str | None] = None
    skrill: Optional[str | None] = None
    ecopayz: Optional[str | None] = None
    webmoney_id: Optional[str | None] = None
    wallets: Optional[str | None] = None
    old: Optional[bool | None] = None
    fund: FoundRead
    nicknameOld: Optional[str | None] = None
    comments: Optional[str | None] = None
    country: Optional[str | None] = None
    town: Optional[str | None] = None
    address: Optional[str | None] = None
    model_config = ConfigDict(from_attributes=False)
    created_at: Optional[datetime | None] = None
    fund: FoundRead
class RecordRead(RecordBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime | None] = None
    created_by: Optional[UserRead | None] = None
    previous_versions: Optional[List[RecordHistoryRead] | None] = None


class RecordUpdate(RecordBase): ...
