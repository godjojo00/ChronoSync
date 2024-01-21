from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from database import shares_collection
from bson import ObjectId

router = APIRouter(tags=["shares"])

class Share(BaseModel):
    calendar_id: str
    shared_with: str  # 可以是用户ID或邮箱等标识
    permissions: str  # 例如 'read', 'write', 'admin' 等

@router.post("/shares/")
async def share_calendar(share: Share):
    shares_collection.insert_one(share.dict())
    return {"message": "Calendar shared successfully"}

@router.get("/shares/", response_model=List[Share])
async def get_shared_calendars():
    # 这里应该基于当前用户的标识来过滤共享
    # 假设 'current_user_id' 是当前用户的标识
    current_user_id = "current_user_id"  # 需要替换成实际用户标识的获取方式
    return list(shares_collection.find({"shared_with": current_user_id}))

@router.put("/shares/{id}")
async def update_share(id: str, share: Share):
    result = shares_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": share.dict()},
        return_document=True
    )
    if result:
        return {"message": "Share updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Share not found")

@router.delete("/shares/{id}")
async def cancel_share(id: str):
    result = shares_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return {"message": "Share cancelled successfully"}
    else:
        raise HTTPException(status_code=404, detail="Share not found")
