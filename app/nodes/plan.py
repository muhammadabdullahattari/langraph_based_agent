import re
from app.state.agent_state import AgentState
from app.nodes.trace import add_trace


def extract_post_id(task: str) -> int | None:
    match = re.search(r"\bpost\s+(\d+)\b", task)

    if not match:
        return None

    return int(match.group(1))


def plan_node(state: AgentState) -> dict:
    task = state["task"].lower()

    if "delete" in task and "post" in task:
        post_id = extract_post_id(task)

        if post_id is None:
            return {
                "plan": "Unable to determine which post to delete.",
                "error": "Post ID is missing.",
                "completed": True,
                "trace": add_trace(state, "plan")
            }

        return {
            "plan": f"Delete post {post_id}.",
            "tool_name": "delete",
            "tool_input": {
                "post_id": post_id,
            },
            "requires_approval": True,
            "trace": add_trace(state, "plan")
        }

    if "calculate" in task:
        return {
            "plan": "Use the calculator tool.",
            "tool_name": "calculator",
            "tool_input": {
                "a": 10,
                "b": 5,
                "operation": "multiply",
            },
            "trace": add_trace(state, "plan")
        }

    if "post" in task or "database" in task:
        post_id = extract_post_id(task)

        if post_id is None:
            return {
                "plan": "Unable to determine which post to search.",
                "error": "Post ID is missing.",
                "completed": True,
                "trace": add_trace(state, "plan")
            }

        return {
            "plan": f"Look up post {post_id} in the database.",
            "tool_name": "search_database",
            "tool_input": {
                "post_id": post_id,
            },
            "trace": add_trace(state, "plan")
        }

    if "search" in task:
        return {
            "plan": "Search the web.",
            "tool_name": "web_search",
            "tool_input": {
                "query": task,
            },
            "trace": add_trace(state, "plan")
        }

    if "fail" in task:
        return {
            "plan": "Execute the failing tool.",
            "tool_name": "failing_tool",
            "tool_input": {
                "message": "Forced failure for testing.",
            },
            "trace": add_trace(state, "plan")
        }

    return {
        "plan": "No matching tool was found.",
        "error": "Unable to determine which tool to use.",
        "completed": True
    }