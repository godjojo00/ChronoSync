from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from database import engine
from . import user

app = FastAPI()
app.include_router(user.router)
origins = [
    'http://localhost:3000',
    "http://localhost"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello Router"}