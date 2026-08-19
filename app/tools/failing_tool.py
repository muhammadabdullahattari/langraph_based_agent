from langchain_core.tools import tool

@tool
def failing_tool(message: str) -> str:
    """A tool that always fails for testing error handling."""
    raise RuntimeError(f"Forced tool failure: {message}")