from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List
from database import calendar_collection  # 使用 calendar_collection
from bson import ObjectId

router = APIRouter(
    tags=["calendar"]
)

class Calendar(BaseModel):
    name: str
    owner: str

class Event(BaseModel):
    title: str
    description: str
    start_date: str
    end_date: str
    calendar_id: str

@router.post("/calendars/")
async def create_calendar(calendar: Calendar):
    if calendar_collection.find_one({"name": calendar.name}):
        raise HTTPException(status_code=400, detail="Calendar already exists")
    calendar_collection.insert_one(calendar.dict())
    return {"msg": "Calendar created successfully"}

@router.get("/calendars/", response_model=List[Calendar])
async def get_calendars():
    return list(calendar_collection.find())

@router.post("/events/")
async def create_event(event: Event):
    # 确保 calendar_id 是 ObjectId
    if not calendar_collection.find_one({"_id": ObjectId(event.calendar_id)}):
        raise HTTPException(status_code=404, detail="Calendar not found")
    # 可能需要一个专门的事件集合
    calendar_collection.insert_one(event.dict())
    return {"msg": "Event created successfully"}

@router.get("/events/{calendar_id}", response_model=List[Event])
async def get_events(calendar_id: str):
    # 也许这里应该查询一个专门的事件集合
    return list(calendar_collection.find({"calendar_id": ObjectId(calendar_id)}))
