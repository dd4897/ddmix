from fastapi import APIRouter, HTTPException,Body
from app.schemas.conversation import Conversation,ChatInput
from app.config.db import conversation_collection
import os
from uuid import uuid4
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
router = APIRouter()
_ = load_dotenv(find_dotenv())
openai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


@router.post("/chat", response_model=Conversation, response_description="Chat with GPT")
async def chat_completion(chat_input: ChatInput = Body(...)):
    # 从数据库中检索用户的最近6条对话
    previous_conversations = await conversation_collection.find(
        {"user_id": chat_input.user_id}
    ).sort("update_time", -1).limit(6).to_list(None)
    # 如果存在以前的对话，将其逆序加入到messages中，因为我们要最早的消息在前
    messages = []
    if previous_conversations:
        for conv in reversed(previous_conversations):
            messages.append({"role": conv["role"], "content": conv["content"]})

    # 添加当前用户的提示
    messages.append({"role": "user", "content": chat_input.prompt})
    try:
        # 使用openai库调用ChatGPT
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0
        )
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=str(e))
    # 解析ChatGPT的响应
    chatgpt_response = response.choices[0].message.content
    # 创建对话记录
    conversation = Conversation(
        session_id=str(uuid4()),  # 此处生成session_id，您可以根据需要进行更改
        user_id=chat_input.user_id,
        model="gpt-3.5-turbo",
        answer_id=str(uuid4()),
        parent_id=None,  # 如果此消息是对另一个消息的回复，则设置相应的parent_id
        prompt=chat_input.prompt,
        role="assistant",  # 假设AI的角色为'assistant'
        content=chatgpt_response,
        update_time=datetime.now(),
        create_time=datetime.now()
    )
    # 将对话保存到MongoDB
    await conversation_collection.insert_one(conversation.dict())
    # 返回Conversation模型作为响应体
    return conversation

