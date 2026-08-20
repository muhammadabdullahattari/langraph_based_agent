from app.state.agent_state import AgentState
from app.nodes.trace import add_trace

def fallback_node(state: AgentState) -> dict:
    reason = state.get("error","The agent could not safely complete the request.")
    message = ("I couldn't safely complete this request because the maximum number of tool calls was reached.")

    return {
        "fallback_reason": reason,
        "result": message,
        "completed": True,
        "trace": add_trace(state, "fallback"),
    }