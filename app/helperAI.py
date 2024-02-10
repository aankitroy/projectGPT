from openai import OpenAI
from app.config import settings
    
client = OpenAI(api_key=settings.OPEN_AI_API_KEY)
def get_assistant_by_id(assistant_id: str):
    assistant = client.beta.assistants.retrieve(assistant_id)
    return assistant