from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from database import events_collection
from bson import ObjectId

router = APIRouter(tags=["events"])

class Event(BaseModel):
    title: str
    description: str
    start_date: str
    end_date: str
    calendar_id: str

@router.post("/events/")
async def create_event(event: Event):
    events_collection.insert_one(event.dict())
    return {"message": "Event created successfully"}

@router.get("/events/", response_model=List[Event])
async def get_events(calendar_id: Optional[str] = Query(None)):
    if calendar_id:
        return list(events_collection.find({"calendar_id": calendar_id}))
    else:
        return list(events_collection.find())

@router.put("/events/{id}")
async def update_event(id: str, event: Event):
    result = events_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": event.dict()},
        return_document=True
    )
    if result:
        return {"message": "Event updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Event not found")

@router.delete("/events/{id}")
async def delete_event(id: str):
    result = events_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return {"message": "Event deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Event not found")
