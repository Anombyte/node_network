from src.shared.State import WaitingState, ProcessingState, ReadyState, ErrorState


class InvalidStateException(Exception):
    """Custom exception raised when an invalid state prevents task processing."""

    def __init__(self, message):
        super().__init__(message)


class StateMachine:
    def __init__(self):
        self.current_state = None  # Start with no state
        self.states = {
            "waiting": WaitingState(self),
            "processing": ProcessingState(self),
            "ready": ReadyState(self),
            "error": ErrorState(self),
        }

    # Dependencies is a list of node id's
    def set_initial_state(self, dependencies=None, task=None):
        """
        Determine and set the initial state based on dependencies and tasks.
        """
        if dependencies and any(not dep["resolved"] for dep in dependencies):
            self.transition_to("waiting", "Unresolved dependencies.")
            return

        if task:
            self.transition_to(
                "processing", "Task assigned and all dependencies resolved."
            )
        else:
            self.transition_to(
                "ready", "No task assigned, and all dependencies resolved."
            )

    def update_state(self, dependencies=None, task=None):
        """
        Re-evaluate and set the correct state based on dependencies and tasks.
        """
        self.set_initial_state(dependencies, task)

    def transition_to(self, state_name, reason):
        """
        Transition to a new state with validation and logging.
        """
        if self.current_state and self.current_state.name == state_name:
            # Avoid redundant transitions
            print(
                f"State transition to '{state_name}' ignored: already in this state."
            )  # Replace with logging
            return  # No transition needed

        if state_name not in self.states:
            raise ValueError(f"State '{state_name}' is not recognized.")

        if self.current_state and not self.current_state.can_transition_to(state_name):
            raise ValueError(
                f"Invalid state transition from '{self.current_state.name}' to '{state_name}'."
            )

        self.current_state = self.states[state_name]
        print(
            f"Transitioned to state '{state_name}' due to: {reason}"
        )  # Replace with logging

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
            print("Attempting to resolve error state.")  # Replace with logging
            self.transition_to("ready", "Error resolved.")
        else:
            print("No error state to resolve.")  # Replace with logging

    def set_state(self, state_name):
        """
        Set the current state without checks (internal use only).
        """
        if state_name not in self.states:
            raise ValueError(f"State '{state_name}' is not recognized.")
        self.current_state = self.states[state_name]

    def get_state(self):
        """
        Get the current state.
        """
        return self.current_state
