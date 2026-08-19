from copy import deepcopy

from app.state.agent_state import AgentState


def add_trace(state: AgentState, node: str) -> list[dict]:
    trace = list(state["trace"])

    trace.append(
        {
            "node": node,
            "iteration": state["iteration"],
            "tool": state["tool_name"],
            "result": deepcopy(state["result"]),
            "error": state["error"],
            "completed": state["completed"],
        }
    )

    return trace