from typing import Any, TypedDict

class AgentState(TypedDict):
    messages: list[Any]

    task: str
    plan: str

    tool_name: str | None
    tool_input: dict[str, Any] | None
    tool_result: Any

    tool_results: dict[str, Any]

    result: Any
    completed: bool

    iteration: int
    max_iterations: int

    failure_count: int
    max_failures: int

    error: str | None

    previous_result: Any
    progress_made: bool

    requires_approval: bool
    approval: bool | None

    trace: list[dict[str, Any]]