from fastapi import APIRouter
from todos import Todo
from database import collection_name
from schemas import list_serial
from bson import ObjectId

router = APIRouter()

@router.get("/")
async def get_todos():
    todos = list_serial(collection_name.find())
    return todos