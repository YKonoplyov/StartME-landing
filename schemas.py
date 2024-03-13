from typing import Any, Dict
from pydantic import BaseModel

from fastapi_users import schemas


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
                "id",
            },
        )

    def create_update_dict_superuser(self):
        return model_dump(self, exclude_unset=True, exclude={"id"})
    

class FoundBase(CreateUpdateDictModel):
    name: str
    discord: str
    link: str
    
class FoundCreate(FoundBase):
    ...

class FoundUpdate(FoundBase):
    id: int

class FoundRead(FoundBase):
    id: int