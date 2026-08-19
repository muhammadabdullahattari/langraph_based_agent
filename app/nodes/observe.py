from app.state.agent_state import AgentState
from app.nodes.trace import add_trace

def observe_node(state: AgentState) -> dict:
    if state["error"]:
        return {
            "completed": True,
            "trace": add_trace(state, "observe")
        }

    if state["failure_count"] >= state["max_failures"]:
        return {
            "completed": True,
            "error": "Maximum tool failures reached.",
            "trace": add_trace(state, "observe")
        }

    if state["iteration"] >= state["max_iterations"]:
        return {
            "completed": True,
            "error": "Maximum iterations reached.",
            "trace": add_trace(state, "observe")
        }

    if state["result"] is not None:
        return {
            "completed": True,
            "trace": add_trace(state, "observe")
        }

    return {
        "completed": False,
        "trace": add_trace(state, "observe")
    }