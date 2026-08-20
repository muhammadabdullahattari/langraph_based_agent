from langchain_core.tools import tool
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from app.config import DATABASE_URL
from app.guardrails.sql import validate_sql


class DatabaseInput(BaseModel):
    post_id: int = Field(description="The numeric ID of the post to retrieve.")

engine = create_engine(DATABASE_URL)

@tool(args_schema=DatabaseInput)
def search_database(post_id: int) -> str:
    """
    Use ONLY for structured post records stored in the application database.
    This tool is read-only.
    """
    query = """
        SELECT id, title, content
        FROM posts
        WHERE id = :post_id
    """

    try:
        if post_id == -1:
            raise RuntimeError("Simulated database failure")

        # Day 4 SQL guardrail
        if not validate_sql(query):
            raise ValueError("Blocked SQL operation: destructive SQL statements are not allowed.")

        safe_query = text(query)

        with engine.connect() as connection:
            result = connection.execute(safe_query,{"post_id": post_id}).mappings().first()

        if result is None:
            return f"No post found with id {post_id}."

        return str(dict(result))

    except Exception as exc:
        return f"Database tool failed safely: {exc}"