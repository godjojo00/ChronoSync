from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route import router
# from database import engine

app = FastAPI()
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

app.include_router(router)
# @app.get("/")
# async def root():
#     return {"message": "Hello Router"}