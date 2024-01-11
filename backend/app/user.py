from fastapi import HTTPException, status, APIRouter
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import os

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# MongoDB 連接設定
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/chronosync")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.chronosync  # 替換為您的數據庫名稱
collection = db.users

# 密碼加密設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserIn(BaseModel):
    email: str
    username: str
    password: str

class UserInDB(UserIn):
    hashed_password: str

class UserLogin(BaseModel):
    username: str
    password: str

async def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserIn):
    # 檢查用戶是否已存在
    existing_user = await collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    user_in_db = UserInDB(**user.dict(), hashed_password=await hash_password(user.password))
    await collection.insert_one(user_in_db.dict(exclude={"password"}))
    return {"msg": "User created successfully"}

@router.post("/login")
async def login(user: UserLogin):
    user_in_db = await collection.find_one({"username": user.username})
    if not user_in_db:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    user_in_db = UserInDB(**user_in_db)
    if not await verify_password(user.password, user_in_db.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return {"msg": "User logged in successfully"}

# 在這裡添加更多路由和邏輯
