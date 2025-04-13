from sqlalchemy import (
    Column, Integer, String, ForeignKey
)
from app.database.database import Base
from sqlalchemy.orm import relationship


class GroupModel(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    parent_id = Column(Integer, ForeignKey('devices.id'))
    sub_groups = relationship("Group")


class StudentModel(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)

    group_id = Column(Integer, ForeignKey('groups.id'))
