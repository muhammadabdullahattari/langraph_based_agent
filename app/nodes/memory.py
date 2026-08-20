from app.memory.long_term import LongTermMemory
from app.state.agent_state import AgentState

memory = LongTermMemory()

def retrieve_memory(state: AgentState) -> dict:
    task = state["task"]
    memories = memory.retrieve(query=task,limit=3)
    return {"retrieved_memories": memories}