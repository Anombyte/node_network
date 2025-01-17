from src.shared.NodeRegistry import NodeRegistry

from src.shared.StateMachine import StateMachine
from src.shared.logger_manager import LoggerMixin
from src.shared.utils import get_current_timestamp, get_unique_id


class AI_Node(LoggerMixin):

    def __init__(
        self,
        in_name,
        in_node_id,
        in_description,
        in_priority,
        in_status,
        in_purpose,
        in_node_registry,
        in_task=None,
        in_supported_tasks=None,
        in_dependencies=None,
        in_activity_logs=None,
        in_identity_prompt=None,
        in_state_machine=None,
    ):
        """
        Initialize the AI_Node with state management, logging, and task details.
        """
        super().__init__()  # Initialize loggers

        # Node attributes
        self.name = in_name
        self.task = in_task
        self.dependencies = in_dependencies or []
        self.state_machine = StateMachine()

        self.node_id = in_node_id or get_unique_id()
        self.node_registry = in_node_registry

        self.description = in_description
        self.status = in_status
        self.purpose = in_purpose

        # Additional attributes
        self.supported_tasks = in_supported_tasks or []
        self.activity_logs = in_activity_logs or []
        self.identity_prompt = in_identity_prompt or (
            "You are part of a node network, specialized in {purpose}."
        )
        self.set_priority(in_priority)
        if self.node_registry:
            self.node_registry.register_node(self)
        # Log initialization details
        self.log_node_event(
            self.name,
            self.node_id,
            f"Node initialized with purpose: {self.purpose}, "
            f"supported tasks: {self.supported_tasks}, "
            f"dependencies: {self.dependencies}",
        )

    def update_state(self):
        """
        Update the state of the node based on its dependencies and task.
        """
        self.state_machine.update_state(
            dependencies=self.dependencies,
            task=self.task,
        )

    def set_task(self, task):
        """
        Assign a task to the node if supported. Updates state as needed.
        """
        if not self.is_task_supported(task):
            error_message = f"Task '{task}' is not supported by Node {self.name}."
            self.log_error(error_message)
            raise ValueError(error_message)

        self.task = task
        self.log_node_event(self.name, self.node_id, f"Task set: {task}")
        self.state_machine.update_state()  # Trigger state check after task assignment

    def is_task_supported(self, task):
        """
        Check if a task is supported by the node.
        """
        return task in self.supported_tasks

    def set_priority(self, in_priority):
        """
        Validate and assign priority to the node.
        """
        if in_priority < 1:
            self.log_error("Priority must be >= 1")
            raise ValueError("Priority must be greater than or equal to 1.")
        self.priority = in_priority
        self.log_node_event(
            self.name, self.node_id, f"Priority updated to {self.priority}"
        )

    def process_task(self):
        """
        Process the assigned task if the node is in a valid state and dependencies are valid.
        """

        self.state_machine.validate_task_processing()
        # Check the current state via the state machine
        if self.state_machine.current_state in ["waiting", "inactive"]:
            # Log the reason for waiting or inactivity
            self.log_debugger(
                f"Node {self.name} is in state '{self.state_machine.current_state}'. "
                f"Task processing will not proceed."
            )
            return {
                "status": "waiting",
                "message": f"Node is in state '{self.state_machine.current_state}' and cannot process tasks.",
            }

        # If the state permits processing, validate and handle the task
        try:
            self.log_debugger(
                f"Node {self.name} is starting to process task: {self.task}"
            )

            # Validate dependencies if in a processing-eligible state
            unresolved_dependencies = [
                dep for dep in self.dependencies if not self.check_dependency(dep)
            ]
            if unresolved_dependencies:
                self.state_machine.update_state()  # Update state based on dependencies
                return {
                    "status": "waiting",
                    "message": "Dependencies are unresolved. Task cannot proceed.",
                    "unresolved_dependencies": unresolved_dependencies,
                }

            # Generate and log prompt
            prompt = self.generate_task_prompt()
            self.log_node_event(self.name, self.node_id, f"Generated prompt: {prompt}")

            # Simulate task execution
            output = f"Generated output for task: {self.task}"

            # Log the result
            result = {
                "status": "success",
                "node_id": self.node_id,
                "task": self.task,
                "output": output,
                "timestamp": get_current_timestamp(),
            }
            self.log_activity(f"Processed task: {self.task}", result)
            return result

        except Exception as e:
            # Handle unexpected errors
            self.log_error(f"Task processing failed: {e}")
            self.state_machine.set_state("error")
            return {"status": "error", "message": str(e)}

    def resolve_dependency(self, dependency):
        """
        Mark a dependency as resolved and update state.
        """
        if dependency in self.dependencies:
            self.dependencies.remove(dependency)
            self.log_node_event(
                self.name, self.node_id, f"Dependency resolved: {dependency}"
            )
            self.state_machine.update_state()

    def generate_task_prompt(self):
        """
        Generate a task prompt combining the identity and the task.
        """
        if not self.task:
            raise ValueError("No task assigned to generate a task prompt.")
        return (
            self.identity_prompt.format(purpose=self.purpose)
            + f" Your task is: {self.task}"
        )

    def log_activity(self, activity, details=None):
        """
        Log an activity with a timestamp.
        """
        timestamp = get_current_timestamp()
        self.activity_logs.append(
            {"activity": activity, "timestamp": timestamp, "details": details or {}}
        )
        self.log_node_event(self.name, self.node_id, f"Activity logged: {activity}")

    def clear_error(self, reason, dependency_id=None):
        """
        Clears error conditions and attempts recovery if applicable.
        """
        self.log_node_event(self.name, self.node_id, f"Clearing error: {reason}")

        if dependency_id:
            self.log_debugger(
                f"Attempting to recover missing dependency node with ID '{dependency_id}'."
            )
            # Example logic: Spin up a new node or notify the user/system
            # self.node_registry.register_node(spin_up_new_node(dependency_id))

        # Clear the error and re-evaluate the state
        self.state_machine.transition_to("waiting")

    def check_dependencies(self):
        """
        Check if all dependencies are resolved.
        """
        unresolved = [
            dep for dep in self.dependencies if not self.check_dependency(dep)
        ]
        return len(unresolved) == 0  # Return True if all dependencies are resolved

    def check_dependency(self, dependency_id):
        """
        Checks a single dependency to see if it is resolved.
        """
        # Retrieve the node by its ID
        node = self.node_registry.get_node_by_id(dependency_id)

        if node is None:
            # Log and attempt recovery if the dependency node does not exist
            error_message = f"Dependency node with ID '{dependency_id}' does not exist."
            self.log_error(f"{error_message}\nAttempting to recover...")
            self.clear_error(reason=error_message, dependency_id=dependency_id)
            return False  # Dependency unresolved because the node does not exist

        # Check if the node is in the desired state and status
        is_resolved = (
            node.get_status() == "idle" and node.state_machine.get_state() == "ready"
        )

        if is_resolved:
            return True  # Dependency is resolved if the node meets the criteria

        # Log an info message for unresolved dependencies
        self.log_debugger(
            f"Dependency node with ID '{dependency_id}' is not resolved. "
            f"Status: {node.get_status()}, State: {node.state_machine.get_state()}"
        )
        return False  # Dependency is unresolved if the criteria are not met

    def get_status(self):
        """
        Returns the current status of the task
        """
        return self.status

    def update_status(self):
        """
        Updates the status based on the current state and task progress.
        """
        if self.state_machine.current_state.name == "waiting":
            if self.dependencies:
                self.status = "waiting for dependencies"
            else:
                self.status = "waiting for task"
        elif self.state_machine.current_state.name == "processing":
            self.status = "processing task"
        elif self.state_machine.current_state.name == "ready":
            self.status = "idle"
        elif self.state_machine.current_state.name == "error":
            self.status = "error encountered"
