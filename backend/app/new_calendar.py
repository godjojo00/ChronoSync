from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List
from database import calendar_collection
from bson import ObjectId

router = APIRouter(tags=["calendar"])

class Calendar(BaseModel):
    name: str
    owner: str

@router.post("/calendars/")
async def create_calendar(calendar: Calendar):
    if calendar_collection.find_one({"name": calendar.name}):
        raise HTTPException(status_code=400, detail="Calendar already exists")
    calendar_collection.insert_one(calendar.dict())
    return {"message": "Calendar created successfully"}

@router.get("/calendars/", response_model=List[Calendar])
async def get_calendars():
    return list(calendar_collection.find())

@router.put("/calendars/{id}")
async def update_calendar(id: str, calendar: Calendar):
    result = calendar_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": calendar.dict()},
        return_document=True
    )
    if result:
        return {"message": "Calendar updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Calendar not found")

@router.delete("/calendars/{id}")
async def delete_calendar(id: str):
    result = calendar_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return {"message": "Calendar deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Calendar not found")
