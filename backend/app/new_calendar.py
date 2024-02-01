from fastapi import APIRouter, HTTPException, status, Body, Path
from pydantic import BaseModel
from typing import List
from database import calendar_collection
from bson import ObjectId

router = APIRouter(tags=["calendar"])

# 日历模型
class Calendar(BaseModel):
    name: str
    owner: str

class CalendarCreateResponse(BaseModel):
    calendar_name: str
    calendar_type: str
    owner_name: str

class CalendarShare(BaseModel):
    shared_with_user_id: str

# 创建日历
@router.post("/calendars/{calendar_id}", response_model=CalendarCreateResponse)
async def create_calendar(calendar_id: str, calendar: Calendar):
    if calendar_collection.find_one({"_id": ObjectId(calendar_id)}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Calendar ID already exists")
    calendar_collection.insert_one(calendar.dict())
    return {
        "calendar_name": calendar.name,
        "calendar_type": "public",  # 或是其他逻辑确定的类型
        "owner_name": calendar.owner
    }

# 获取用户日历
@router.get("/calendars/{calendar_id}", response_model=Calendar)
async def get_calendar(calendar_id: str):
    calendar = calendar_collection.find_one({"_id": ObjectId(calendar_id)})
    if calendar:
        return Calendar(**calendar)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar not found")

# 分享日历
@router.post("/calendars/{calendar_id}/share", response_model=CalendarShare)
async def share_calendar(calendar_id: str, share_calendar: CalendarShare):
    # 实际逻辑可能会更复杂，涉及到更新数据库中的共享设置
    shared_calendar = calendar_collection.find_one({"_id": ObjectId(calendar_id)})
    if shared_calendar:
        # 更新数据库逻辑
        return {"shared_with_user_id": share_calendar.shared_with_user_id, "calendar_id": calendar_id}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar not found")

# 删除日历
@router.delete("/calendars/{calendar_id}")
async def delete_calendar(calendar_id: str):
    result = calendar_collection.delete_one({"_id": ObjectId(calendar_id)})
    if result.deleted_count:
        return {"message": "Calendar deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar not found")
