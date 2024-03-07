from pydantic import BaseModel,Field
from typing import Optional
from bson import ObjectId



class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    username: str
    email: Optional[str] = None
    phone: int

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid),  # 这将确保ObjectId被转换成str
        }
        json_schema_extra = {
            "example": {
                "username": "老王头",
                "email": "johndoe@example.com",
                "phone": 17624250830,
                "_id": ""
            }
        }
