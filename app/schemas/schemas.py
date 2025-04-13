from pydantic import BaseModel, ConfigDict
from typing import List


class GroupSchema(BaseModel):
    id: int
    name: str
    parent_id: int
    sub_groups: List["GroupSchema"] = []

    model_config = ConfigDict(from_attributes=True)


class StudentSchema(BaseModel):
    id: int
    name: str
    email: str
    group_id: int
