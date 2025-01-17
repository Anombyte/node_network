from datetime import datetime
import uuid
import functools
import time


def get_current_timestamp():
    """
    Generates the current timestamp.

    Returns:
        str: Current timestamp in ISO 8601 format.
    """
    return datetime.now().isoformat()


def get_unique_id():
    """
    Generates a unique id.
    """
    return str(uuid.uuid4())


# ===========================
# Custom Exceptions
# ===========================


class OrchestratorError(Exception):
    """Base exception for orchestrator-related issues."""

    pass


class NodeError(Exception):
    """Base exception for node-related issues."""

    pass


class MessagingError(Exception):
    """Base exception for messaging system issues."""

    pass


# ===========================
# Decorators
# ===========================


def retry_operation(retry_count=3, retry_delay=2):
    """
    Retries a function in case of an exception.
    :param retry_count: Number of retries.
    :param retry_delay: Delay (in seconds) between retries.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retry_count):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < retry_count - 1:
                        time.sleep(retry_delay)
                    else:
                        raise e

        return wrapper

    return decorator


def fallback_on_error(fallback_func):
    """
    Executes a fallback function if the main function fails.
    :param fallback_func: Alternative function to call.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                return fallback_func(*args, **kwargs)

        return wrapper

    return decorator


# ===========================
# Validation Helpers
# ===========================


def validate_node_config(config):
    """
    Validates a node's configuration.
    :param config: Dictionary of node configuration.
    :raises ValueError: If validation fails.
    """
    required_keys = ["name", "type", "node_id"]
    for key in required_keys:
        if key not in config or not config[key]:
            raise ValueError(f"Missing required key: {key}")


def validate_message(message):
    """
    Validates the structure of a message.
    :param message: Dictionary representing a message.
    :raises ValueError: If the structure is invalid.
    """
    required_keys = ["sender", "receiver", "content"]
    for key in required_keys:
        if key not in message or not message[key]:
            raise ValueError(f"Message is missing key: {key}")
