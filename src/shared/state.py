from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.shared.StateMachine import StateMachine


class BaseState:
    def __init__(self, state_machine: "StateMachine"):
        self.state_machine = state_machine

    @property
    def name(self):
        return self.__class__.__name__.replace("State", "").lower()

    def can_transition_to(self, new_state: str) -> bool:
        """Define valid state transitions."""
        return True  # Allow all transitions by default

    def can_process_task(self):
        """Determine if the state allows task processing."""
        return False  # By default, processing is not allowed in states

    def handle_task(self):
        """Default behavior for handling tasks in a state."""
        self.state_machine.node.log_debugger(
            f"State '{self.name}' does not support task processing."
        )
        return {
            "status": "not_allowed",
            "message": f"Task processing is not allowed in state '{self.name}'.",
        }


class WaitingState(BaseState):
    def can_transition_to(self, new_state):
        return new_state in ["ready", "processing", "error", "inactive"]

    def can_process_task(self):
        """Waiting state does not allow task processing."""
        return False

    def handle_task(self):
        """Handle task logic for waiting state."""
        unresolved_dependencies = [
            dep for dep in self.state_machine.node.dependencies
            if not self.state_machine.node.check_dependency(dep)
        ]
        if unresolved_dependencies:
            self.state_machine.node.log_debugger(
                f"Node is in 'waiting' state due to unresolved dependencies: {unresolved_dependencies}"
            )
            return {
                "status": "waiting",
                "message": "Dependencies are unresolved.",
                "unresolved_dependencies": unresolved_dependencies,
            }
        # If no dependencies are unresolved, update the state.
        self.state_machine.update_state()
        return {"status": "state_updated", "message": "Dependencies resolved. State updated."}


class ReadyState(BaseState):
    def can_transition_to(self, new_state):
        return new_state in ["waiting", "processing", "error", "inactive"]

    def can_process_task(self):
        """Ready state allows task processing."""
        return True

    def handle_task(self):
        """Handle task logic for ready state."""
        if not self.state_machine.node.task:
            self.state_machine.node.log_debugger(
                f"No task assigned for Node {self.state_machine.node.name} in 'ready' state."
            )
            self.state_machine.update_state()
            return {
                "status": "no_task",
                "message": "No task assigned. State re-evaluated.",
            }
        # Transition to processing if a task is available.
        self.state_machine.set_state("processing")
        return self.state_machine.node.process_task()


class ProcessingState(BaseState):
    def can_transition_to(self, new_state):
        return new_state in ["waiting", "ready", "error", "inactive"]

    def can_process_task(self):
        """Processing state allows task processing."""
        return True

    def handle_task(self):
        """Handle task processing in processing state."""
        if not self.state_machine.node.task:
            self.state_machine.node.log_error(
                f"No task assigned in 'processing' state for Node {self.state_machine.node.name}."
            )
            self.state_machine.set_state("error")
            return {
                "status": "error",
                "message": "Processing state reached without a task. Transitioned to error.",
            }
        # Process the task
        return self.state_machine.node.process_task()


class ErrorState(BaseState):
    def can_transition_to(self, new_state):
        return new_state in ["waiting", "ready", "inactive"]

    def can_process_task(self):
        """Error state does not allow task processing."""
        return False

    def handle_task(self):
        """Error state should not process tasks."""
        self.state_machine.node.log_error(
            f"Cannot process tasks in 'error' state for Node {self.state_machine.node.name}."
        )
        return {
            "status": "error",
            "message": "Task processing not allowed in error state.",
        }


class InactiveState(BaseState):
    def can_transition_to(self, new_state):
        return new_state in ["waiting", "ready", "error"]

    def can_process_task(self):
        """Inactive state does not allow task processing."""
        return False

    def handle_task(self):
        """Inactive state does not process tasks."""
        self.state_machine.node.log_debugger(
            f"Node {self.state_machine.node.name} is inactive and cannot process tasks."
        )
        return {
            "status": "inactive",
            "message": "Node is inactive. Task processing is not allowed.",
        }
