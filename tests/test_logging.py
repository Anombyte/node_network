from unittest.mock import patch, MagicMock
import pytest
from src.shared.logger_manager import LoggerMixin


@pytest.fixture
def logger_mixin():
    """
    A fixture to create an instance of LoggerMixin for testing.
    """
    return LoggerMixin()


@patch("logging.getLogger")  # Mock the logger retrieval
def test_logger_initialization(mock_get_logger):
    """
    Test that LoggerMixin initializes the correct loggers.
    """
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    mixin = LoggerMixin()

    # Assert that the loggers were retrieved with the correct names
    mock_get_logger.assert_any_call("default")
    mock_get_logger.assert_any_call("debugger")
    mock_get_logger.assert_any_call("error_logger")
    assert mixin.logger == mock_logger
    assert mixin.debugger == mock_logger
    assert mixin.error_logger == mock_logger


@patch("logging.getLogger")
def test_log_info(mock_get_logger):
    """
    Test that log_info calls the logger's info method with the correct message.
    """
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    mixin = LoggerMixin()
    mixin.log_info("This is an info message.")

    # Verify that the logger.info method was called once with the correct message
    mock_logger.info.assert_called_once_with("This is an info message.")


@patch("logging.getLogger")
def test_log_error(mock_get_logger):
    """
    Test that log_error calls the error_logger's error method with the correct message.
    """
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    mixin = LoggerMixin()
    mixin.log_error("This is an error message.")

    # Verify that the error_logger.error method was called once with the correct message
    mock_logger.error.assert_called_once_with("This is an error message.")


@patch("logging.getLogger")
def test_log_task_event(mock_get_logger):
    """
    Test that log_task_event logs the correct task-specific message.
    """
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    mixin = LoggerMixin()
    mixin.log_task_event(task_name="ExampleTask", in_id=42, message="Task started.")

    # Verify that the logger.info method was called with the formatted message
    mock_logger.info.assert_called_once_with("[Task-ExampleTask - 42] Task started.")


@patch("logging.getLogger")
def test_log_node_event(mock_get_logger):
    """
    Test that log_node_event logs the correct node-specific message.
    """
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    mixin = LoggerMixin()
    mixin.log_node_event(node_name="ExampleNode", in_id=99, message="Node initialized.")

    # Verify that the logger.info method was called with the formatted message
    mock_logger.info.assert_called_once_with(
        "[Node-ExampleNode - 99] Node initialized."
    )
