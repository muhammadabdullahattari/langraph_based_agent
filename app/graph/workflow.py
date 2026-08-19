from langgraph.graph import END, START, StateGraph
from app.memory.checkpoint import create_checkpointer
from app.nodes import act_node,delete_node,observe_node,plan_node
from app.state.agent_state import AgentState

def route_after_plan(state: AgentState) -> str:
    if state["error"]:
        return "end"

    if state["requires_approval"]:
        return "delete"

    return "act"


def route_after_observe(state: AgentState) -> str:
    if state["error"]:
        return "end"

    if state["completed"]:
        return "end"

    if state["iteration"] >= state["max_iterations"]:
        return "end"

    if state["failure_count"] >= state["max_failures"]:
        return "end"

    return "act"


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("plan", plan_node)
    builder.add_node("act", act_node)
    builder.add_node("observe", observe_node)
    builder.add_node("delete", delete_node)

    builder.add_edge(START, "plan")

    builder.add_conditional_edges("plan",route_after_plan,{"act": "act","delete": "delete","end": END})
    builder.add_edge("act", "observe")

    builder.add_conditional_edges("observe",route_after_observe,{"act": "act","end": END,})
    builder.add_edge("delete", END)

    return builder.compile(checkpointer=create_checkpointer(),interrupt_before=["delete"])