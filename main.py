from app.graph import build_graph
from app.state.agent_state import AgentState


def create_state(task: str) -> AgentState:
    return {
        "messages": [],

        "task": task,
        "plan": "",

        "tool_name": None,
        "tool_input": None,
        "tool_result": None,

        "tool_results": {},

        "result": None,
        "completed": False,

        "iteration": 0,
        "max_iterations": 5,

        "failure_count": 0,
        "max_failures": 2,

        "error": None,

        "previous_result": None,
        "progress_made": True,

        "requires_approval": False,
        "approval": None,

        "trace": [],
    }


def print_result(state: AgentState) -> None:
    if state["error"]:
        print(f"\nAgent Error: {state['error']}")
        return

    if state["result"] is not None:
        print(f"\nAgent: {state['result']}")
        return

    print("\nAgent: I could not complete the request.")


def main() -> None:
    graph = build_graph()

    thread_id = "chat-session-1"

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    print("Agent started.")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("\nAgent: Goodbye!")
            break

        if not user_input:
            continue

        initial_state = create_state(user_input)

        graph.invoke(
            initial_state,
            config=config,
        )

        checkpoint = graph.get_state(config)


        if checkpoint.next == ("delete",):

            print("\nAgent: This operation requires your approval.")
            print(
                f"Agent: Are you sure you want to "
                f"delete post {checkpoint.values['tool_input']['post_id']}?"
            )

            approval = input("Approve? (yes/no): ").strip().lower()

            if approval in {"yes", "y"}:

                graph.update_state(
                    config,
                    {
                        "approval": True,
                    }
                )

                graph.invoke(
                    None,
                    config=config
                )

            else:
                graph.update_state(
                    config,
                    {
                        "approval": False,
                        "error": "Operation rejected by user.",
                        "completed": True,
                    }
                )

        final_state = graph.get_state(config)
        print_result(final_state.values)

        print()


if __name__ == "__main__":
    main()