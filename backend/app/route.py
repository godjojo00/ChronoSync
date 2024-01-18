from fastapi import APIRouter
from todos import Todo
from database import users_collection
from schemas import list_serial
from bson import ObjectId

router = APIRouter()

@router.get("/")
async def get_todos():
    todos = list_serial(users_collection.find())
    return todos