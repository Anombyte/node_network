from shared import state
from shared.Logger import Logger
    
import uuid  # Import uuid for generating unique identifiers

class Node:

    # Initialize a logger for this class
    logger = Logger()

    def __init__(self, in_name, in_node_id, in_description, in_priority, in_status, in_purpose):
        """
        Constructor for the Node class.

        Parameters:
        - in_node_id (str): Optional unique identifier for the node. If not provided, a UUID is generated.
        - in_description (str): Description of the node.
        - in_priority (int): Priority level of the node. Default is 1.
        - in_status (str): Current status of the node. Default is "active".
        - in_purpose (str): Purpose or role of the node.
        """
        # Default values for readability
        node_id = None
        name = ""
        description = ""
        priority = 1
        status = "active"
        purpose = in_purpose
        logger = None

        # Assign class attributes
        self.name = in_name
        self.node_id = in_node_id or str(uuid.uuid4())  # Use provided ID or generate a UUID
        self.description = in_description
        self.priority = in_priority
        self.status = in_status
        self.purpose = in_purpose
        
        # Set up the logger
        self._setup_logger()

    def get_details(self):
        """
        Retrieves details of the node.

        Returns:
        A dictionary containing the node's attributes: node_id, description, priority, status, and purpose.
        """
        return {
            "node_id": self.node_id,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "purpose": self.purpose,
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
        self.logger.log_node_event(self.name, f"Status updated to {self.status}")

    def __str__(self):
        """
        Provides a readable string representation of the Node object.

        Returns:
        A string showing the node ID, priority, status, and purpose.
        """
        return f"Node({self.node_id}, Priority={self.priority}, Status={self.status}, Purpose={self.purpose})"
















def task(input_text, node_name):
    """
    Summarizer GPT function.
    """
    logger.info(f"{node_name}: Task execution started.")
    summary = f"Summary of: {input_text}"  # Replace with actual GPT summarization logic.
    state["nodes"][node_name]["output"] = summary
    state["nodes"][node_name]["status"] = "Completed"
    logger.info(f"{node_name}: Task completed with output: {summary}")


