from pydantic import BaseModel
from datetime import datetime


class ChatInput(BaseModel):
    user_id: str
    prompt: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "65e965c6b867bf9dccd0fce6",
                "prompt": "你好"
            }
        }


class Conversation(BaseModel):
    session_id: str  # 会话id
    user_id: str
    model: str = "gpt-3.5-turbo"
    answer_id: str | None
    parent_id: str | None
    prompt: str
    role: str
    content: str
    update_time: datetime
    create_time: datetime
