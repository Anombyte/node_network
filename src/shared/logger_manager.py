import logging
import logging.config
import threading  # For explicit locking if needed
from src.shared.utils import get_current_timestamp

# Global lock for logging operations
_logger_lock = threading.Lock()


def configure_logging():
    """
    Configures the logging system for the application.
    """
    with _logger_lock:  # Ensure the configuration is thread-safe
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
        """Log an informational event."""
        with _logger_lock:
            self.logger.info(message)

    def log_error(self, message):
        """Log an error event."""
        with _logger_lock:
            self.error_logger.error(f"Error: {message}")

    def log_task_event(self, task_name, in_id=None, message=""):
        """Log a task-specific event."""
        with _logger_lock:
            log_message = f"[Task-{task_name} - {in_id}] {message}"
            self.logger.info(log_message)

    def log_node_event(self, node_name, in_id=None, message=""):
        """Log a node-specific event."""
        with _logger_lock:
            log_message = f"[Node-{node_name} - {in_id}] {message}"
            self.logger.info(log_message)

    def log_debugger(self, in_name, in_id=None, message=""):
        """Log a debugger-specific event."""
        with _logger_lock:
            log_message = f"[Node-{in_name} - {in_id}] {message}"
            self.debugger.debug(log_message)

    def log_state_transition(self, in_name, from_state, to_state, in_id=None):
        """Log state transitions with structured logging."""
        with _logger_lock:
            log_message = {
                "event": "state_transition",
                "from_state": str(from_state),
                "to_state": str(to_state),
                "timestamp": get_current_timestamp(),
                "name": in_name,
                "ID": in_id,
            }
            self.debugger.debug(log_message)
