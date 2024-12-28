import logging

def configure_logger(name="Logger", level=logging.INFO):
    """
    Configures the logger with a specific format and handler.

    Parameters:
    - name (str): The name of the logger.
    - level (int): The logging level (default: INFO).
    """
    logger = logging.getLogger(name)

    if not logger.hasHandlers():  # Avoid adding duplicate handlers
        # Set log level
        logger.setLevel(level)

        # Create a console handler
        handler = logging.StreamHandler()

        # Define the log message format
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(handler)

    return logger


def log_event(message, in_logger_name):
    """
    Log a general informational event.

    Parameters:
    - message (str): The message to log.
    - in_logger_name (str): The name of the logger (default: "Logger").
    """
    logger = logging.getLogger(in_logger_name)
    logger.info(message)


def log_error(error_message, in_logger_name):
    """
    Log an error event.

    Parameters:
    - error_message (str): The error message to log.
    - in_logger_name (str): The name of the logger (default: "Logger").
    """
    logger = logging.getLogger(in_logger_name)
    logger.error(error_message)


def log_task_event(task_name, in_id = None, in_logger_name = "Logger", in_message = ""):
    """
    Log a node-specific event.

    Parameters:
    - task_name (str): The name of the node.
    - message (str): The message to log.
    - node_id (optional): An optional node ID.
    - in_logger_name (str): The name of the logger (default: "Logger").
    """
    message = in_message
    node_id = in_id
    logger = logging.getLogger(in_logger_name)
    logger.info(f"[Node-{task_name} - {node_id}] {message}")


def log_node_event(node_name, in_id = None, in_logger_name = "Logger", in_message = ""):
    """
    Log a node-specific event.

    Parameters:
    - node_name (str): The name of the node.
    - message (str): The message to log.
    - node_id (optional): An optional node ID.
    - in_logger_name (str): The name of the logger (default: "Logger").
    """
    message = in_message
    node_id = in_id
    logger = logging.getLogger(in_logger_name)
    logger.info(f"[Node-{node_name} - {node_id}] {message}")
