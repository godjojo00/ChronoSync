from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from typing import Optional
from database import events_collection
from bson import ObjectId
import datetime

router = APIRouter(tags=["events"])

# Event model for creation
class EventCreate(BaseModel):
    name: str
    event_type: str
    content: str
    start_time: datetime.datetime
    end_time: datetime.datetime

# Event model for response
class EventResponse(BaseModel):
    id: str = Field(..., alias='_id')
    name: str
    event_type: str
    content: str
    start_time: datetime.datetime
    end_time: datetime.datetime

# Create an event
@router.post("/event/{calendar_id}", response_model=EventResponse)
async def create_event(calendar_id: str, event: EventCreate):
    event_dict = event.dict()
    event_dict['calendar_id'] = calendar_id
    result = events_collection.insert_one(event_dict)
    created_event = events_collection.find_one({"_id": result.inserted_id})
    if created_event:
        return EventResponse(**created_event)
    else:
        raise HTTPException(status_code=500, detail="Event creation failed")

# Retrieve an event
@router.get("/event/{event_id}", response_model=EventResponse)
async def get_event(event_id: str):
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    if event:
        return EventResponse(**event)
    else:
        raise HTTPException(status_code=404, detail="Event not found")

