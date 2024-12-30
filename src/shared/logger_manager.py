import logging
import logging.config


def configure_logging():
    """
    Configures the logging system for the application.
    """
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "detailed": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "detailed",
                },
                "file": {
                    "level": "INFO",
                    "class": "logging.FileHandler",
                    "filename": "app.log",
                    "formatter": "detailed",
                },
            },
            "loggers": {
                "default": {
                    "handlers": ["console", "file"],
                    "level": "INFO",
                    "propagate": False,
                },
                "debugger": {
                    "handlers": ["console"],
                    "level": "DEBUG",
                    "propagate": False,
                },
                "error_logger": {
                    "handlers": ["file"],
                    "level": "ERROR",
                    "propagate": False,
                },
            },
            "root": {
                "handlers": ["console", "file"],
                "level": "WARNING",
            },
        }
    )


class LoggerMixin:
    """
    Mixin class to provide pre-configured loggers and reusable logging methods.
    """

    def __init__(
        self,
        logger_name="default",
        debugger_name="debugger",
        error_logger_name="error_logger",
    ):
        self.logger = logging.getLogger(logger_name)
        self.debugger = logging.getLogger(debugger_name)
        self.error_logger = logging.getLogger(error_logger_name)

    def log_info(self, message):
        """
        Log an informational event.

        Parameters:
        - message (str): The message to log.
        """
        self.logger.info(message)

    def log_error(self, message):
        """
        Log an error event.

        Parameters:
        - message (str): The message to log.
        """
        self.error_logger.error(message)

    def log_task_event(self, task_name, in_id=None, message=""):
        """
        Log a task-specific event.

        Parameters:
        - task_name (str): The name of the task.
        - in_id (optional): An optional task ID.
        - message (str): The message to log.
        """
        log_message = f"[Task-{task_name} - {in_id}] {message}"
        self.logger.info(log_message)

    def log_node_event(self, node_name, in_id=None, message=""):
        """
        Log a node-specific event.

        Parameters:
        - node_name (str): The name of the node.
        - in_id (optional): An optional node ID.
        - message (str): The message to log.
        """
        log_message = f"[Node-{node_name} - {in_id}] {message}"
        self.logger.info(log_message)

    def log_debugger(self, in_name, in_id=None, message=""):
        """
        Log a node-specific event.

        Parameters:
        - node_name (str): The name of the node.
        - in_id (optional): An optional node ID.
        - message (str): The message to log.
        """
        log_message = f"[Node-{in_name} - {in_id}] {message}"
        self.debugger.debug(log_message)