from langchain_core.tools import tool
from pydantic import BaseModel, Field

class WebSearchInput(BaseModel):
    query: str = Field(description="A question or search query requiring external web information.")

@tool(args_schema=WebSearchInput)
def web_search(query: str) -> str:
    """
    Use ONLY when external web information is required.
    Do not use for application database records or local documents.
    """
    return f"Web search stub result for: {query}"