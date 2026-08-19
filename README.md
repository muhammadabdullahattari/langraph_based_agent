# LangGraph Stateful Agent

A practical LangGraph project for building stateful, graph-based agents.

## Features

- StateGraph
- Shared state
- Nodes and edges
- Conditional routing
- Cyclic workflows
- Max iteration guard
- Failure handling
- Checkpointing
- Thread-based state
- Pause / Resume
- Human approval
- Tool result memory
- Execution tracing

## Project Structure

```text
langraph/
├── main.py
├── README.md
├── .gitignore
├── requirements.txt
│
└── app/
    ├── graph/
    │   └── workflow.py
    │
    ├── state/
    │   └── agent_state.py
    │
    ├── nodes/
    │   ├── plan.py
    │   ├── act.py
    │   ├── observe.py
    │   ├── delete.py
    │   └── trace.py
    │
    ├── memory/
    │   └── checkpoint.py
    │
    └── tools/
        ├── calculator.py
        ├── database.py
        ├── web_search.py
        └── failing_tool.py