from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY

def get_llm() -> ChatGroq:
    return ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=GROQ_API_KEY,
        temperature=0
    )