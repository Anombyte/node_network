from shared.logger_manager import LoggerMixin

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
        in_task,
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

    def set_task(self, in_task):
        # TODO validate task is a task that this node can process
        self.task = in_task

    def set_priority(self, in_priority):
        # Validate and assign priority
        if in_priority >= 1:
            self.priority = in_priority
        else:
            self.log_error("Priority must be >= 1")
            raise ValueError("Priority must be greater than or equal to 1.")

    def process_task(self):
        """
        Stub for processing the assigned task.

        Returns:
            str: Placeholder result indicating task is processed.
        """
        self.log_node_event(
            f"Processing task for Node {self.name} (ID: {self.node_id})"
        )
        return "Task processed"
