from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from database import db, users_collection
from bson import ObjectId

# 密碼上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 用戶模型
class UserInDB(BaseModel):
    username: str
    email: str
    hashed_password: str

class UserIn(BaseModel):
    username: str
    email: str
    password: str

# 用戶路由
router = APIRouter(
    tags=["users"]
)

# 密碼加密函數
def hash_password(password):
    return pwd_context.hash(password)

# 密碼驗證函數
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 註冊用戶
@router.post("/register")
async def register_user(user: UserIn):
    # 檢查用戶名是否已存在
    if db["users"].find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")

    # 密碼加密並創建用戶
    hashed_password = hash_password(user.password)
    new_user = UserInDB(**user.dict(), hashed_password=hashed_password)
    db["users"].insert_one(new_user.dict(exclude={"password"}))

    return {"msg": "User registered successfully"}

# 用戶登錄
@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db["users"].find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return {"msg": "User logged in successfully"}