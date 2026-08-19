from app.state.agent_state import AgentState
from app.nodes.trace import add_trace
from app.tools import calculator,search_database,failing_tool,web_search

TOOLS = {
    "calculator": calculator,
    "search_database": search_database,
    "failing_tool": failing_tool,
    "web_search": web_search,
}


def act_node(state: AgentState) -> dict:
    tool_name = state["tool_name"]
    tool_input = state["tool_input"]

    if not tool_name:
        return {"error": "No tool selected.", "completed": True}

    if tool_name not in TOOLS:
        return {
            "error": f"Unknown tool: {tool_name}",
            "completed": True,
            "trace": add_trace(state, "act")
        }

    cache_key = f"{tool_name}:{tool_input}"

    if cache_key in state["tool_results"]:
        result = state["tool_results"][cache_key]

        return {
            "previous_result": state["result"],
            "result": result,
            "tool_result": result,
            "progress_made": False,
            "trace": add_trace(state, "act")
        }

    try:
        tool = TOOLS[tool_name]

        result = tool.invoke(tool_input or {})
        tool_results = dict(state["tool_results"])
        tool_results[cache_key] = result

        return {
            "previous_result": state["result"],
            "result": result,
            "tool_result": result,
            "tool_results": tool_results,
            "progress_made": True,
            "iteration": state["iteration"] + 1,
            "trace": add_trace(state, "act")
        }

    except Exception as exc:
        return {
            "error": str(exc),
            "failure_count": state["failure_count"] + 1,
            "iteration": state["iteration"] + 1,
            "progress_made": False,
            "trace": add_trace(state, "act")
        }