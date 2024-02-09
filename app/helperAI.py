from openai import OpenAI
from dotenv import load_dotenv
import os
import time
from app.config import settings

client = OpenAI(settings.OPEN_AI_API_KEY)

def connect_to_openAI():
    client = OpenAI(settings.OPEN_AI_API_KEY)
    
def get_assistant_by_id(assistant_id: str):
    global client
    if client is None:
        connect_to_openAI()
    assistant = client.beta.assistants.retrieve(assistant_id)
    return assistant
    
    
