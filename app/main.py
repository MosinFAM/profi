from fastapi import FastAPI
from sqlalchemy import select
from fastapi.responses import JSONResponse
from app.logger import logger
from app.database.database import lifespan, SessionDep
from app.models.models import (
    StudentModel, GroupModel
)
from app.schemas.schemas import (
    StudentSchema, GroupSchema
)


app = FastAPI(lifespan=lifespan)


@app.get("/students", response_model=list[StudentSchema])
async def get_all_students(session: SessionDep):
    query = select(StudentModel)
    result = await session.execute(query)
    students = result.scalars().all()
    logger.info("Fetched %d students", len(students))
    list_of_students = list()
    for student in students:
        list_of_students.append({"id": student.id,
                                 "groupr_id": student.group_id,
                                 "name": student.name})
    return list_of_students


@app.get("/groups", response_model=list[GroupSchema])
async def get_all_devices(session: SessionDep):
    query = select(GroupModel)
    result = await session.execute(query)
    groups = result.scalars().all()
    logger.info("Fetched %d groups", len(groups))
    return groups


@app.post("/students")
async def create_student(data: StudentSchema, session: SessionDep):
    students = StudentModel(name=data.name,
                            email=data.email,
                            group_id=data.group_id)
    session.add(students)
    await session.commit()
    logger.info("Created user with id=%d", students.id)
    return JSONResponse({"id": students.id,
                         "groupr_id": students.group_id,
                         "name": students.name})


@app.post("/groups")
async def add_group(data: GroupSchema, session: SessionDep):
    group = GroupModel(name=data.name,
                       parent_id=data.parent_id,
                       name=data.name)
    session.add(group)
    await session.commit()
    logger.info("Created device with id=%d for user_id=%d", group.id,
                data.user_id)
    return JSONResponse({"id": group.id,
                         "parent_id": group.parent_id,
                         "name": group.name})
