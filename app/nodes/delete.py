from app.state.agent_state import AgentState
from app.nodes.trace import add_trace

def delete_node(state: AgentState) -> dict:
    if state["approval"] is not True:
        return {
            "error": "Delete operation was not approved.",
            "completed": True,
            "trace": add_trace(state, "delete")
        }

    post_id = state["tool_input"]["post_id"]

    return {
        "result": f"Post {post_id} deleted successfully.",
        "completed": True,
        "trace": add_trace(state, "delete")
    }