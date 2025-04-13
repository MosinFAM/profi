from fastapi import FastAPI, HTTPException
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
async def get_all_users(session: SessionDep):
    query = select(StudentModel)
    result = await session.execute(query)
    users = result.scalars().all()
    logger.info("Fetched %d users", len(users))
    return users


@app.get("/groups", response_model=list[GroupSchema])
async def get_all_devices(session: SessionDep):
    query = select(GroupModel)
    result = await session.execute(query)
    devices = result.scalars().all()
    logger.info("Fetched %d devices", len(devices))
    return devices


@app.post("/students")
async def create_user(data: StudentSchema, session: SessionDep):
    user = StudentModel(name=data.name)
    session.add(user)
    await session.commit()
    logger.info("Created user with id=%d", user.id)
    return JSONResponse({"ok": True, "user_id": user.id})


@app.post("/groups")
async def add_device(data: GroupSchema, session: SessionDep):

    user_exists = await session.get(StudentModel, data.user_id)
    if not user_exists:
        logger.warning("Attempt to create device for non-existent user_id=%d",
                       data.user_id)
        raise HTTPException(status_code=404, detail="User not found")

    new_device = GroupModel(
        name=data.name,
        user_id=data.user_id,
    )
    session.add(new_device)
    await session.commit()
    logger.info("Created device with id=%d for user_id=%d", new_device.id,
                data.user_id)
    return JSONResponse({"ok": True, "device_id": new_device.id})
