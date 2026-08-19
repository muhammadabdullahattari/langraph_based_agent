from langchain_core.tools import tool
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    expression: str = Field(
        description="A mathematical expression such as '25 * 40' or '100 / 4'."
    )

@tool(args_schema=CalculatorInput)
def calculator(expression: str) -> str:
    """Use ONLY for mathematical calculations."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as exc:
        return f"Calculation error: {exc}"