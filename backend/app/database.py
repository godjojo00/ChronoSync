from pymongo import MongoClient

uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client.chronosync

users_collection = db["users"]
calendar_collection = db["calendar"]
events_collection = db["events"]