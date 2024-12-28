import logging
from io import StringIO
import pytest
from shared.logger_utils import configure_logger, log_event, log_error, log_task_event, log_node_event

@pytest.fixture
def log_stream():
    """
    A pytest fixture to provide a logger and a StringIO stream to capture log outputs.
    """
    logger_name = "TestLogger"
    log_stream = StringIO()

    # Configure the logger for testing
    logger = configure_logger(name=logger_name, level=logging.DEBUG)
    for handler in logger.handlers:
        logger.removeHandler(handler)  # Ensure no duplicate handlers

    # Add a stream handler to capture log output
    stream_handler = logging.StreamHandler(log_stream)
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger_name, log_stream


def test_configure_logger():
    """
    Test that the logger is configured correctly.
    """
    logger = configure_logger(name="MyLogger", level=logging.WARNING)
    assert logger.name == "MyLogger"
    assert logger.level == logging.WARNING


def test_log_event(log_stream):
    """
    Test logging an informational event.
    """
    logger_name, stream = log_stream
    log_event("This is a test event.", logger_name)
    stream.seek(0)
    log_output = stream.read()
    assert "INFO" in log_output
    assert "This is a test event." in log_output


def test_log_error(log_stream):
    """
    Test logging an error event.
    """
    logger_name, stream = log_stream
    log_error("This is a test error.", logger_name)
    stream.seek(0)
    log_output = stream.read()
    assert "ERROR" in log_output
    assert "This is a test error." in log_output


def test_log_task_event_with_id(log_stream):
    """
    Test logging a task-specific event with an ID.
    """
    logger_name, stream = log_stream
    log_task_event(task_name="Task1", in_id=42, in_logger_name=logger_name, in_message="Task completed.")
    stream.seek(0)
    log_output = stream.read()
    assert "INFO" in log_output
    assert "[Node-Task1 - 42] Task completed." in log_output


def test_log_task_event_without_id(log_stream):
    """
    Test logging a task-specific event without an ID.
    """
    logger_name, stream = log_stream
    log_task_event(task_name="Task1", in_logger_name=logger_name, in_message="Task started.")
    stream.seek(0)
    log_output = stream.read()
    assert "INFO" in log_output
    assert "[Node-Task1 - None] Task started." in log_output


def test_log_node_event_with_id(log_stream):
    """
    Test logging a node-specific event with an ID.
    """
    logger_name, stream = log_stream
    log_node_event(node_name="Node1", in_id=99, in_logger_name=logger_name, in_message="Node initialized.")
    stream.seek(0)
    log_output = stream.read()
    assert "INFO" in log_output
    assert "[Node-Node1 - 99] Node initialized." in log_output


def test_log_node_event_without_id(log_stream):
    """
    Test logging a node-specific event without an ID.
    """
    logger_name, stream = log_stream
    log_node_event(node_name="Node1", in_logger_name=logger_name, in_message="Node shutdown.")
    stream.seek(0)
    log_output = stream.read()
    assert "INFO" in log_output
    assert "[Node-Node1 - None] Node shutdown." in log_output
