import pytest
from unittest.mock import patch
from src.shared.AI_Node import AI_Node  # Corrected import path


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


# --------------------------- Node Initialization Tests --------------------------- #

@patch("uuid.uuid4")  # Mock UUID generation
def test_node_initialization_with_uuid(mock_uuid4):
    """Test that the node initializes correctly with a generated UUID if no node_id is provided."""
    mock_uuid4.return_value = "mocked-uuid"

    node = AI_Node(
        in_name="Node1",
        in_node_id=None,  # No node ID provided
        in_description="Test description",
        in_priority=5,
        in_status="active",
        in_purpose="Testing",
        in_task="Test Task",
    )

    # Assertions
    assert node.node_id == "mocked-uuid"
    assert node.status == "active"
    assert node.priority == 5


# --------------------------- process_task Tests --------------------------- #

def test_process_task_happy_path(sample_node):
    """Test that process_task works correctly when a task is assigned."""
    sample_node.task = "Sample Task"

    # Call process_task
    result = sample_node.process_task()

    # Assertions
    assert result["status"] == "success"
    assert result["task"] == "Sample Task"
    assert "output" in result
    assert "timestamp" in result


def test_process_task_no_task_assigned(sample_node):
    """Test that process_task returns an error when no task is assigned."""
    # Call process_task without assigning a task
    result = sample_node.process_task()

    # Assertions
    assert result["status"] == "error"
    assert result["message"] == "No task assigned."


@patch("src.shared.AI_Node.AI_Node.execute_task")  # Mock execute_task with correct import path
def test_process_task_execution_error(mock_execute, sample_node):
    """Test that process_task handles execution errors gracefully."""
    sample_node.task = "Sample Task"

    # Simulate an exception in execute_task
    mock_execute.side_effect = Exception("Execution failed")

    # Call process_task
    result = sample_node.process_task()

    # Assertions
    assert result["status"] == "error"
    assert "Execution failed" in result["message"]


@patch("src.shared.AI_Node.get_current_timestamp", return_value="2024-01-01T00:00:00")
def test_process_task_logging(mock_get_timestamp, sample_node):
    """Test that process_task includes the correct timestamp in its output."""
    sample_node.task = "Sample Task"
    result = sample_node.process_task()

    # Assertions
    assert result["timestamp"] == "2024-01-01T00:00:00"


# --------------------------- execute_task Tests --------------------------- #

def test_execute_task(sample_node):
    """Test that execute_task generates the correct output."""
    task = "Sample Task"
    output = sample_node.execute_task(task)

    # Assertions
    assert output == f"Generated output for task: {task}"


# --------------------------- set_priority Tests --------------------------- #

@pytest.mark.parametrize(
    "priority, expected_result",
    [
        (10, 10),  # Valid priority
        (1, 1),    # Valid priority
    ],
)
def test_set_priority_valid(sample_node, priority, expected_result):
    """Test that set_priority accepts valid priorities."""
    sample_node.set_priority(priority)
    assert sample_node.priority == expected_result


@pytest.mark.parametrize(
    "priority, expected_exception",
    [
        (-5, ValueError),  # Invalid priority
        (0, ValueError),   # Invalid priority
    ],
)
def test_set_priority_invalid(sample_node, priority, expected_exception):
    """Test that set_priority raises exceptions for invalid priorities."""
    with pytest.raises(expected_exception, match="Priority must be greater than or equal to 1."):
        sample_node.set_priority(priority)
