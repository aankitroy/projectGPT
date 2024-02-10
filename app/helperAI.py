import shelve
import time
from openai import OpenAI
from app.config import settings
    
client = OpenAI(api_key=settings.OPEN_AI_API_KEY)
def get_assistant_by_id(assistant_id: str):
    assistant = client.beta.assistants.retrieve(assistant_id)
    return assistant

'''
def create_assistant(assistant):
    """
    You currently cannot set the temperature for Assistant via the API.
    """
    assistant = client.beta.assistants.create(
        name=assistant.name,
        instructions=assistant.instructions,
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview",
        file_ids=[file.id],
    )
    return assistant
'''



def check_if_thread_exists(wa_id):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(wa_id, None)
    
def remove_if_thread_exists(wa_id):
    with shelve.open("threads_db") as threads_shelf:
        threads_shelf['wa_id'] = None
        return


def store_thread(wa_id, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[wa_id] = thread_id
        
        
def generate_response(message_body, wa_id, email, assistant):
    # Check if there is already a thread_id for the wa_id
    thread_id = check_if_thread_exists(wa_id)

    # If a thread doesn't exist, create one and store it
    if thread_id is None:
        print(f"Creating new thread for {email} with wa_id {wa_id}")
        thread = client.beta.threads.create()
        store_thread(wa_id, thread.id)
        thread_id = thread.id

    # Otherwise, retrieve the existing thread
    else:
        print(f"Retrieving existing thread for {email} with wa_id {wa_id}")
        thread = client.beta.threads.retrieve(thread_id)

    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    # Run the assistant and get the new message
    new_message = run_assistant(thread, assistant)
    print(f"To {email}:", new_message)
    return new_message


def run_assistant(thread, assistant):

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        instructions="Your role is to carefully delineate software development requirements based on initial inputs. You must infer critical components and are authorized to seek additional information for clarity. "+
"Workflow:"+
"Initial Requirements Capture: The user will share basic requirements. Utilize this data as a foundation for crafting more detailed specifications."+
"Detailed Inquiry for Clarity: Should the user's input be insufficient or vague, initiate a dialogue to gather essential details that refine your comprehension, aiming to perfect the requirements. "+
"Detailed Analysis: Examine the user responses meticulously. If ambiguities persist or further information is necessary, loop back to the inquiry stage (Step 2). This process is iterative until a thorough understanding is established. Analyze the rough estimation in hours. "+
"Synthesize Requirements: Upon obtaining all necessary information, succinctly formulate the software requirements in a clear, concise manner, in the range of 100-250 words document with rough estimation in hours. This document must encapsulate all vital details to ensure clear understanding by Software Engineers and Product Managers. "+
"Note: The task is to be executed remotely and should include an estimated completion time. If tasks exceed the 1-2 hour maximum estimate, break them down into subtasks that each fit within a 1-hour timeframe and mention the effort estimation along with the individual tasks. "+
"Do not ask about the budget. "+
"Do not ask about maintenance and support. "+
"Do not ask about timeline expectations. ",
        assistant_id=assistant.id,
    )

    # Wait for completion
    while run.status != "completed":
        # Be nice to the API
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    print(f"Generated message: {new_message}")
    return new_message
