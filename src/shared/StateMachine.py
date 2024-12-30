from typing import Optional
from src.shared.State import BaseState, WaitingState, ProcessingState, ReadyState, ErrorState
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.shared.AI_Node import AI_Node


class InvalidStateException(Exception):
    """Custom exception raised when an invalid state prevents task processing."""
    def __init__(self, message):
        super().__init__(message)


#Initialises the StateMachine for the AINode in order to dynamically update the nodes state for task processing
#Initial state begins as a BaseState parent class, so any of the child classes can be imported 
# e.g. Initialise the AI_Nodes StateMachine with ProcessingState as we have assigned an initial task instead of starting in
#"ReadyState" or No State
class StateMachine:
    def __init__(self, node: "AI_Node"):
        self.node = node
        self.current_state = BaseState(self)
        self.states = {
            "waiting": WaitingState(self),
            "processing": ProcessingState(self),
            "ready": ReadyState(self),
            "error": ErrorState(self),
        }
        self.set_initial_state()

    def set_initial_state(self):
        """Set the initial state based on node's dependencies and tasks."""
        self.update_state()

    def update_state(self):
        """
        Automatically re-evaluate and set the correct state.
        Checks dependencies and tasks to determine the appropriate state.
        """
        if self.node.dependencies:
            unresolved = [dep for dep in self.node.dependencies if not self.node.check_dependency(dep)]
            if unresolved:
                self.transition_to("waiting", f"Unresolved dependencies: {unresolved}")
                return

        if self.node.task:
            self.transition_to("processing", "Task assigned and all dependencies resolved.")
        else:
            self.transition_to("ready", "No task assigned, and all dependencies resolved.")

    def set_state(self, state_name):
        """
        Set the current state without checks (internal use only).
        """
        if state_name not in self.states:
            raise ValueError(f"State '{state_name}' is not recognized.")
        self.current_state = self.states[state_name]

    def transition_to(self, state_name, reason):
        """
        Transition to a new state with validation and logging.
        """
        if self.current_state and self.current_state.name == state_name:
            # Avoid redundant transitions
            self.node.log_debugger(
                f"State transition to '{state_name}' ignored: already in this state."
            )
            return  # No transition needed

        if state_name not in self.states:
            raise ValueError(f"State '{state_name}' is not recognized.")

        if self.current_state and not self.current_state.can_transition_to(state_name):
            raise ValueError(
                f"Invalid state transition from '{self.current_state.name}' to '{state_name}'."
            )

        self.current_state = self.states[state_name]
        self.node.log_node_event(
            self.node.name,
            self.node.node_id,
            f"Transitioned to state '{state_name}' due to: {reason}",
        )

    def validate_task_processing(self):
        """
        Validate if the task can be processed in the current state.
        Throws an exception if the state does not allow processing.
        """
        if not self.current_state or not self.current_state.can_process_task():
            raise InvalidStateException(
                f"Cannot process task in state '{self.current_state.name}'."
            )

    def resolve_error(self):
        """
        Attempt to resolve the error and transition to a valid state.
        """
        if isinstance(self.current_state, ErrorState):
            # Perform error resolution logic
            self.node.log_node_event(
                self.node.name,
                self.node.node_id,
                "Attempting to resolve error state.",
            )

            # Clear error condition and re-evaluate state
            self.node.clear_error()
            self.update_state()
        else:
            self.node.log_debugger(
                f"Node {self.node.name} (ID: {self.node.node_id}) is not in an error state. No resolution needed."
            )

    def get_state(self):
        return self.current_state

