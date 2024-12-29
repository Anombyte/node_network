import pytest
from unittest.mock import patch
from src.shared.AI_Node import AI_Node


@pytest.fixture
def sample_node():
    """Fixture to provide a sample AI_Node instance."""
    return AI_Node(
        in_name="TestNode",
        in_node_id="1234",
        in_description="Sample Node for Tests",
        in_priority=1,
        in_status="active",
        in_purpose="Testing",
        in_task=None,
    )


# --------------------------- AI_Node Logging Tests --------------------------- #

@patch("src.shared.AI_Node.AI_Node.log_node_event")
def test_set_priority_logs(mock_log_node_event, sample_node):
    """Test that set_priority logs the correct message."""
    sample_node.set_priority(10)
    mock_log_node_event.assert_called_once_with(
        "TestNode", "1234", "Priority updated to 10"
    )


@patch("src.shared.AI_Node.AI_Node.log_error")
@pytest.mark.parametrize(
    "priority, expected_message",
    [
        (0, "Priority must be >= 1"),
        (-5, "Priority must be >= 1"),
    ],
)
def test_set_priority_logs_error(mock_log_error, sample_node, priority, expected_message):
    """Test that set_priority logs an error for invalid priorities."""
    with pytest.raises(ValueError):
        sample_node.set_priority(priority)
    mock_log_error.assert_called_once_with(expected_message)


@patch("src.shared.AI_Node.get_current_timestamp", return_value="2024-01-01T00:00:00")
@patch("src.shared.AI_Node.AI_Node.log_node_event")
@patch("src.shared.AI_Node.AI_Node.log_error")
def test_process_task_logging(
    mock_log_error, mock_log_node_event, mock_get_timestamp, sample_node
):
    """Test that process_task logs events for valid and invalid tasks."""
    # Case 1: No task assigned
    sample_node.task = None
    sample_node.process_task()
    mock_log_error.assert_called_once_with(
        "No task assigned to Node TestNode (ID: 1234)."
    )
    mock_log_error.reset_mock()

    # Case 2: Valid task assigned
    sample_node.task = "Sample Task"
    sample_node.process_task()

    # Assertions for logging
    mock_log_node_event.assert_any_call(
        "TestNode", "1234", "Processing task: Sample Task"
    )
    mock_log_node_event.assert_any_call(
        "TestNode",
        "1234",
        "Task completed successfully: {'status': 'success', 'node_id': '1234', "
        "'task': 'Sample Task', 'output': 'Generated output for task: Sample Task', "
        "'timestamp': '2024-01-01T00:00:00'}",
    )


@patch("src.shared.AI_Node.AI_Node.log_error")
def test_process_task_logs_error_on_exception(mock_log_error, sample_node):
    """Test that process_task logs an error if execute_task raises an exception."""
    sample_node.task = "Sample Task"

    # Mock execute_task to raise an exception
    with patch.object(
        sample_node, "execute_task", side_effect=Exception("Execution failed")
    ):
        sample_node.process_task()

    mock_log_error.assert_called_once_with(
        "Error processing task in Node TestNode: Execution failed"
    )
