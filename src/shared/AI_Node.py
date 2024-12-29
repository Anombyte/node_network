from shared.logger_manager import LoggerMixin
from src.shared.utils import get_current_timestamp
import uuid  # Import uuid for generating unique identifiers


class AI_Node(LoggerMixin):
    def __init__(
        self,
        in_name,
        in_node_id,
        in_description,
        in_priority,
        in_status,
        in_purpose,
        in_task=None,
        in_supported_tasks=None,
        in_dependencies=None,
        in_activity_logs=None,
        in_identity_prompt=None,
    ):
        """
        Constructor for the Node class.

        Parameters:
        - in_node_id (str): Optional unique identifier for the node. If not provided, a UUID is generated.
        - in_description (str): Description of the node.
        - in_priority (int): Priority level of the node. Default is 1.
        - in_status (str): Current status of the node. Default is "active".
        - in_purpose (str): Purpose or role of the node.
        """

        super().__init__()  # Initialize loggers from LoggerMixin which include 'default', 'debugger' and 'error_logger'

        # Assign class attributes
        self.name = in_name
        self.node_id = in_node_id or str(
            uuid.uuid4()
        )  # Use provided ID or generate a UUID
        self.description = in_description
        self.status = in_status
        self.purpose = in_purpose
        self.task = in_task
        self.set_priority(in_priority)

        self.supported_tasks = in_supported_tasks or []
        self.dependencies = in_dependencies or []
        self.activity_logs = in_activity_logs or []
        self.identity_prompt = (
            in_identity_prompt
            or "You are part of a node network, specialized in {purpose}."
        )

    def get_details(self):
        """
        Retrieves details of the node.

        Returns:
        A dictionary containing the node's attributes: node_id, description, priority, status, and purpose.
        """
        self.log_node_event(
            self.name,
            self.node_id,
            f"Details retrieved...\n Description: {self.description}\n Priority: {self.priority}\n Purpose: {self.purpose} Current Task: {self.task}",
        )

        return {
            "node_id": self.node_id,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "purpose": self.purpose,
            "task": self.task,  # TODO make task an Object
        }

    def set_status(self, in_status):
        """
        Updates the node's status.

        Parameters:
        - in_status (str): The new status of the node.

        Logs the status update.
        """
        # Update the node's status.
        self.status = in_status

        # Log the status update.
        self.log_node_event(self.name, self.node_id, f"Status updated to {self.status}")

    def __str__(self):
        """
        Provides a readable string representation of the Node object.

        Returns:
        A string showing the node ID, priority, status, and purpose.
        """
        outString = f"Node({self.node_id}, Priority={self.priority}, Status={self.status}, Purpose={self.purpose}, Task={self.task})"
        self.log_node_event(self.name, self.node_id, outString)
        return outString

    def set_task(self, task):
        """
        Assign a task to the node if it is supported.

        Parameters:
            task (str): The task to assign.
        
        Raises:
            ValueError: If the task is not supported by the node.
        """
        if not self.is_task_supported(task):
            error_message = f"Task '{task}' is not supported by Node {self.name}."
            self.log_error(error_message)
            raise ValueError(error_message)
        
        self.task = task
        self.log_node_event(self.name, self.node_id, f"Task set: {task}")

    def is_task_supported(self, task):
        """
        Check if a given task is supported by the node.

        Parameters:
            task (str): The task to check.
        
        Returns:
            bool: True if the task is supported, False otherwise.
        """
        # Match task against supported_tasks (can be extended for more complex logic)
        # TODO: AI Shenanigans will happen here to turn task into one of the task types I think if we even keep this
        return task in self.supported_tasks

    def set_priority(self, in_priority):
        # Validate and assign priority
        if in_priority >= 1:
            self.priority = in_priority
            # Log the priority update
            self.log_node_event(self.name, self.node_id, f"Priority updated to {self.priority}")
        else:
            self.log_error("Priority must be >= 1")
            raise ValueError("Priority must be greater than or equal to 1.")

    def process_task(self):
        """Process the assigned task."""
        if not self.task:
            self.log_error(f"No task assigned to Node {self.name} (ID: {self.node_id}).")
            return {"status": "error", "message": "No task assigned."}

        # Check dependencies
        if self.dependencies:
            unresolved = [dep for dep in self.dependencies if not self.check_dependency(dep)]
            if unresolved:
                self.log_error(f"Unresolved dependencies for Node {self.name}: {unresolved}")
                return {"status": "error", "message": "Unresolved dependencies."}

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

    def generate_task_prompt(self):
        """Generate a task prompt combining the identity and the task."""
        if not self.task:
            raise ValueError("No task assigned to generate a task prompt.")
        return self.identity_prompt.format(purpose=self.purpose) + f" Your task is: {self.task}"

    def score_response(self, response):
        """Score a response based on node-specific criteria."""
        # Example: Security nodes might penalize insecure patterns
        return {"score": 85, "feedback": "Secure but lacks HTTPS enforcement."}
    
    def check_dependency(self, dependency_id):
        """Check if a dependency is resolved."""
        # Placeholder logic
        return True

    def log_activity(self, activity, details=None):
        """Log an activity."""
        timestamp = get_current_timestamp()
        self.activity_logs.append({"activity": activity, "timestamp": timestamp, "details": details or {}})
        self.log_node_event(self.name, self.node_id, f"Activity logged: {activity}")
