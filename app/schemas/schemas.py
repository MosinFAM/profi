from pydantic import BaseModel, ConfigDict
from typing import List


class GroupSchema(BaseModel):
    id: int
    name: str
    sub_groups: List["GroupSchema"] = []

    model_config = ConfigDict(from_attributes=True)


class StudentSchema(BaseModel):
    id: int
    name: str
    group_id: int
