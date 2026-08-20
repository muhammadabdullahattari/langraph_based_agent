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
    tool_call_count = state.get("tool_call_count", 0)
    max_tool_calls = state.get("max_tool_calls", 5)
    
    tool_name = state["tool_name"]
    tool_input = state["tool_input"]
    
    if tool_call_count >= MAX_TOOL_CALLS:
        return {
            "tool_limit_reached": True,
            "error": "Maximum tool-call limit of 5 reached.",
            "completed": True,
        }
        
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
        tool_call_count += 1

        return {
            "tool_call_count": tool_call_count,
            "tool_limit_reached": tool_call_count >= max_tool_calls,
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