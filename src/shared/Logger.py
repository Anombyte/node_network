import logging

class Logger:
    """
    A wrapper class for Python's logging module to provide reusable, encapsulated logging functionality.
    """

    def __init__(self, in_name):
        """
        Initialize the Logger instance.

        Parameters:
        - in_name (str): The name of the logger, typically the module or class name.
        """
        # Default Values
        name = ""

        # Assign the name for the logger
        self.name = in_name

        # Create the logger instance with the given name
        self.logger = logging.getLogger(name, id)

        # Configure the logger
        self._configure_logger()

    def _configure_logger(self):
        """
        Configures the logger with a specific format and handler.
        """
        # Set the log level
        self.logger.setLevel(logging.INFO)

        # Create a console handler
        handler = logging.StreamHandler()

        # Define the format for log messages
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Attach the formatter to the handler
        handler.setFormatter(formatter)

        # Add the handler to the logger
        if not self.logger.handlers:  # Avoid adding duplicate handlers
            self.logger.addHandler(handler)

    def log_event(self, message):
        """
        Log a general informational event.
        """
        self.logger.info(message)

    def log_error(self, error_message):
        """
        Log an error event.
        """
        self.logger.error(error_message)

    def log_task_event(self, node_name, message):
        """
        Log a task-specific event.

        Parameters:
        - node_name (str): The name of the node associated with the task.
        - message (str): The message to log.
        """
        self.logger.info(f"[Task-{node_name}] {message}")

    def log_node_event(self, node_name, message):
        """
        Log a node-specific event.

        Parameters:
        - node_name (str): The name of the node.
        - message (str): The message to log.
        """
        self.logger.info(f"[Node-{node_name}] {message}")
