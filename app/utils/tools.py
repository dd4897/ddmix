import uuid
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
def get_uuid():
    return uuid.uuid4()

_ = load_dotenv(find_dotenv())
openai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)