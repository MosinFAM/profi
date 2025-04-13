from fastapi import FastAPI, HTTPException
from sqlalchemy import select, delete, update
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


@app.get("/students", response_model=list[StudentSchema])
async def get_all_students(session: SessionDep):
    query = select(StudentModel)
    result = await session.execute(query)
    await session.commit()
    students = result.scalars().all()
    logger.info("Fetched %d students", len(students))
    list_of_students = list()
    for student in students:
        list_of_students.append({"id": student.id,
                                 "groupr_id": student.group_id,
                                 "name": student.name})
    return list_of_students


@app.get("/students/{student_id}", response_model=list[StudentSchema])
async def get_students_by_id(student_id: int, session: SessionDep):
    query = select(StudentModel).where(StudentModel.id == student_id)
    result = await session.execute(query)
    await session.commit()
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="student not found")
    return JSONResponse({"id": student.id,
                         "parent_id": student.group_id,
                         "name": student.name})


@app.put("/students/{student_id}", response_model=list[StudentSchema])
async def put_students_by_id(student_id: int,
                             data: StudentSchema,
                             session: SessionDep):
    query = update(StudentModel).where(StudentModel.id == student_id).values(
        name=data.name,
        email=data.email,
        group_id=data.group_id
    )
    result = await session.execute(query)
    await session.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="student not found")
    return JSONResponse({"id": student_id,
                         "parent_id": data.group_id,
                         "name": data.name})


@app.delete("/students/{student_id}", response_model=list[StudentSchema])
async def delete_students_by_id(student_id: int, session: SessionDep):
    query = delete(StudentModel).where(StudentModel.id == student_id)
    result = await session.execute(query)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="student not found")
    return JSONResponse({"message": "deleted"})


@app.get("/groups", response_model=list[GroupSchema])
async def get_all_devices(session: SessionDep):
    query = select(GroupModel)
    result = await session.execute(query)
    groups = result.scalars().all()
    logger.info("Fetched %d groups", len(groups))
    return groups


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


@app.get("/groups/{group_id}", response_model=GroupSchema)
async def get_group(group_id: int, session: SessionDep):
    query = select(GroupModel).where(GroupModel.id == group_id)
    result = await session.execute(query)
    group = result.scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    logger.info("Fetched group with id=%d", group.id)
    return {"id": group.id, "parent_id": group.parent_id, "name": group.name}


@app.delete("/groups/{group_id}")
async def delete_group(group_id: int, session: SessionDep):
    query = delete(GroupModel).where(GroupModel.id == group_id)
    result = await session.execute(query)
    await session.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Group not found")
    logger.info("Deleted group with id=%d", group_id)
    return JSONResponse({"message": "deleted"})


@app.put("/groups/{group_id}", response_model=GroupSchema)
async def put_group(group_id: int, data: GroupSchema, session: SessionDep):
    query = update(GroupModel).where(GroupModel.id == group_id).values(
        name=data.name,
        parent_id=data.parent_id
    )
    result = await session.execute(query)
    await session.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Group not found")

    logger.info("Updated group with id=%d", group_id)
    return {"id": group_id, "parent_id": data.parent_id, "name": data.name}
