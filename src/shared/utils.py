from datetime import datetime


def get_current_timestamp():
    """
    Generates the current timestamp.

    Returns:
        str: Current timestamp in ISO 8601 format.
    """
    return datetime.now().isoformat()