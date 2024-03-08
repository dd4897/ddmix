from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
# MongoDB 配置
MONGO_DETAILS = "mongodb://localhost:27017/ddmix"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.ddmix
user_collection = database.get_collection("user")
conversation_collection = database.get_collection("conversations")  # 'conversations' 是我们MongoDB中存储对话的集合
