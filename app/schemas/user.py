from pydantic import BaseModel

class User(BaseModel):
    id:str
    username:str
    email:str = None
    phone:int
    class Config:
        schema_extra = {
            "example": {
                "name": "老王头",
                "email": "johndoe@example.com",
                "phone": 17624250830
            }
        }