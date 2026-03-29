from crewai import LLM
import os
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def chat_with_ai(user_input, context=""):

    prompt = f"""
    You are an intelligent AI Career Assistant.

    Context (User's Career Plan):
    {context}

    User Question:
    {user_input}

    Instructions:
    - Be helpful and concise
    - Give practical suggestions
    - Personalize using context
    """

    response = llm.call(prompt)
    return response