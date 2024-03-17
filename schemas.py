from datetime import datetime
from typing import Any, Dict, Optional, List
from pydantic import BaseModel

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
            exclude={
                "id"
            },
        )

    def create_update_dict_superuser(self):
        return model_dump(self, exclude_unset=True, exclude={"id"})

    
    def convert_fields_to_optional(self):
        return {k: Optional[v] for k, v in self.__annotations__.items()}


    

class FoundBase(CreateUpdateDictModel):
    name: str
    discord: str
    link: str
    
class FoundCreate(FoundBase):
    ...

class FoundUpdate(FoundBase):
     
    name: Optional[str|None] = None
    discord: Optional[str|None] = None
    link: Optional[str|None] = None

class FoundRead(FoundBase):
    id: int


class UserRead(users_schemas.BaseUser):
    id: int
    username: str
    role: Roles
    email: Optional[str|None] = None
    first_name: Optional[str|None] = None
    last_name: Optional[str|None] = None
    by_fathers_name: Optional[str|None] = None
    contact_fields: Optional[dict|None] = None
    address: Optional[str|None] = None
    created_at: datetime
    gipsy_team: Optional[str|None] = None


class UserCreate(users_schemas.BaseUserCreate):
    username: str
    role: Roles
    email: Optional[str|None] = None
    first_name: Optional[str|None] = None
    last_name: Optional[str|None] = None
    by_fathers_name: Optional[str|None] = None
    contact_fields: Optional[dict|None] = None
    address: Optional[str|None] = None
    created_at: datetime
    gipsy_team: Optional[str|None] = None

class UserUpdate(users_schemas.BaseUserUpdate):
    email: Optional[str|None] = None
    role: Roles
    email: Optional[str|None] = None
    first_name: Optional[str|None] = None
    last_name: Optional[str|None] = None
    by_fathers_name: Optional[str|None] = None
    contact_fields: Optional[dict|None] = None
    address: Optional[str|None] = None
    created_at: datetime
    gipsy_team: Optional[str|None] = None

# class UserRead(users_schemas.CreateUpdateDictModel):
#     ...


class RecordBase(CreateUpdateDictModel):
    arbitrage: Optional[str|None] = None
    comment: Optional[str|None] = None

class RecordCreate(RecordBase):
    user_id: int
    found_id: int

class RecordHistoryRead(RecordBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime|None] = None
    user: UserRead
    found: FoundRead

class RecordRead(RecordBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime|None] = None
    user: UserRead
    found: FoundRead
    previous_versions: Optional[List["RecordHistoryRead"]|None] = None

class RecordUpdate(RecordBase):
    ...
