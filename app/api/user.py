from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.config.db import user_collection
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

router = APIRouter()

# Pydantic 模型，用于请求与响应
class User(BaseModel):
    id: str = None
    name: str
    email: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "johndoe@example.com"
            }
        }

# 创建用户
@router.post("/users/", response_description="Add new user", response_model=User)
async def create_user(user: User) -> User:
    user = jsonable_encoder(user)
    new_user = await user_collection.insert_one(user)
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return created_user

# 获取所有用户
@router.get("/users/", response_description="List all users", response_model=List[User])
async def list_users():
    users = await user_collection.find().to_list(1000)
    return [user for user in users]

# 获取指定用户
@router.get("/users/{id}", response_description="Get a single user", response_model=User)
async def find_user(id: str):
    if (user := await user_collection.find_one({"_id": ObjectId(id)})) is not None:
        return user
    raise HTTPException(status_code=404, detail=f"User {id} not found")

# 更新用户
@router.put("/users/{id}", response_description="Update a user", response_model=User)
async def update_user(id: str, user: User):
    user = {k: v for k, v in user.dict().items() if v is not None}

    if len(user) >= 1:
        update_result = await user_collection.update_one({"_id": ObjectId(id)}, {"$set": user})

        if update_result.modified_count == 1:
            if (
                updated_user := await user_collection.find_one({"_id": ObjectId(id)})
            ) is not None:
                return updated_user

    if (existing_user := await user_collection.find_one({"_id": ObjectId(id)})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"User {id} not found")

# 删除用户
@router.delete("/users/{id}", response_description="Delete a user")
async def delete_user(id: str):
    delete_result = await user_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return True
    raise HTTPException(status_code=404, detail=f"User {id} not found")
