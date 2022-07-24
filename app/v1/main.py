from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from typing import List

from . import schema

import os
import motor.motor_asyncio
router = APIRouter(prefix="/api/v1")

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGODB_URL'))
db = client.crud
crud = db.get_collection("crud")

@router.post("/create", response_description="Create", response_model=schema.StudentModel)
async def create(student: schema.StudentModel):
   student = jsonable_encoder(student)
   new_student = await crud.insert_one(student)
   created_student = await crud.find_one({"_id": new_student.inserted_id})
   return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)


@router.get(
    "/", response_description="List all", response_model=List[schema.StudentModel]
)
async def list_students():
    students = await crud.find().to_list(1000)
    return students

@router.get(
    "/{id}", response_description="Get a single data", response_model=schema.StudentModel
)
async def show_student(id: str):
    if (student := await crud.find_one({"_id": id})) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"student {id} not found")

@router.put("/{id}", response_description="Update a single data", response_model=schema.StudentModel)
async def update_student(id: str, student: schema.UpdateStudentModel):
    student = {k: v for k, v in student.dict().items() if v is not None}

    if len(student) >= 1:
        update_result = await crud.update_one({"_id": id}, {"$set": student})

        if update_result.modified_count == 1:
            if (
                updated_student := await db["crud"].find_one({"_id": id})
            ) is not None:
                return updated_student

    if (existing_student := await crud.find_one({"_id": id})) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f"student {id} not found")

@router.delete("/{id}", response_description="Delete a student")
async def delete_student(id: str):
    delete_result = await crud.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"student {id} not found")