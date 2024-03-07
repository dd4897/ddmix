from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
# MongoDB 配置
MONGO_DETAILS = "mongodb://localhost:27017/ddmix"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.users
user_collection = database.get_collection("user")

