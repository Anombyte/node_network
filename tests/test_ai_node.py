import pytest
from unittest.mock import patch, MagicMock
from src.shared.AI_Node import AI_Node  # Corrected import path
from src.shared.StateMachine import InvalidStateException


# --------------------------- Fixtures --------------------------- #

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
        in_supported_tasks=["task1", "task2"],
        in_dependencies=["dep1", "dep2"],
    )


@pytest.fixture
def mocked_registry():
    """Fixture for a mocked NodeRegistry."""
    mocked_registry = MagicMock()
    mocked_registry.get_node_by_id.side_effect = lambda node_id: None if node_id == "missing" else MagicMock()
    return mocked_registry


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
    assert node.name == "Node1"


# --------------------------- Dependency Handling Tests --------------------------- #

def test_check_dependency_resolved(mocked_registry):
    """Test check_dependency returns True for resolved dependencies."""
    node = AI_Node(
        in_name="TestNode",
        in_node_id="1234",
        in_description="Sample Node",
        in_priority=1,
        in_status="active",
        in_purpose="Testing",
        in_node_registry=mocked_registry,
    )
    dependency_mock = MagicMock()
    dependency_mock.get_status.return_value = "idle"
    dependency_mock.state_machine.get_state.return_value = "ready"
    mocked_registry.get_node_by_id.return_value = dependency_mock

    assert node.check_dependency("dep1") is True


def test_check_dependency_unresolved(mocked_registry):
    """Test check_dependency returns False for unresolved dependencies."""
    node = AI_Node(
        in_name="TestNode",
        in_node_id="1234",
        in_description="Sample Node",
        in_priority=1,
        in_status="active",
        in_purpose="Testing",
        in_node_registry=mocked_registry,
    )
    dependency_mock = MagicMock()
    dependency_mock.get_status.return_value = "processing"
    dependency_mock.state_machine.get_state.return_value = "waiting"
    mocked_registry.get_node_by_id.return_value = dependency_mock

    assert node.check_dependency("dep1") is False


def test_check_dependency_missing(mocked_registry):
    """Test check_dependency returns False and logs an error for missing dependencies."""
    node = AI_Node(
        in_name="TestNode",
        in_node_id="1234",
        in_description="Sample Node",
        in_priority=1,
        in_status="active",
        in_purpose="Testing",
        in_node_registry=mocked_registry,
    )
    mocked_registry.get_node_by_id.return_value = None

    assert node.check_dependency("missing") is False


# --------------------------- Task Processing Tests --------------------------- #

def test_process_task_happy_path(sample_node):
    """Test that process_task works correctly when a task is assigned."""
    sample_node.task = "task1"
    sample_node.dependencies = []
    sample_node.state_machine.validate_task_processing = MagicMock()  # Mock state validation
    sample_node.generate_task_prompt = MagicMock(return_value="Generated Prompt")

    result = sample_node.process_task()

    # Assertions
    assert result["status"] == "success"
    assert result["task"] == "task1"
    assert "output" in result
    assert "timestamp" in result


def test_process_task_with_unresolved_dependencies(sample_node):
    """Test that process_task handles unresolved dependencies."""
    sample_node.dependencies = ["dep1"]
    sample_node.check_dependency = MagicMock(return_value=False)  # Mock unresolved dependency

    result = sample_node.process_task()

    # Assertions
    assert result["status"] == "waiting"
    assert "unresolved_dependencies" in result
    assert "dep1" in result["unresolved_dependencies"]


def test_process_task_fails_state_validation(sample_node):
    """Test that process_task raises an exception if the state does not allow processing."""
    sample_node.state_machine.validate_task_processing = MagicMock(side_effect=InvalidStateException("Invalid state"))

    with pytest.raises(InvalidStateException, match="Invalid state"):
        sample_node.process_task()


@patch("src.shared.AI_Node.get_current_timestamp", return_value="2024-01-01T00:00:00")
def test_process_task_logs(mock_get_timestamp, sample_node):
    """Test that process_task includes the correct timestamp in its output."""
    sample_node.task = "task1"
    sample_node.state_machine.validate_task_processing = MagicMock()  # Mock state validation

    result = sample_node.process_task()

    # Assertions
    assert result["timestamp"] == "2024-01-01T00:00:00"


# --------------------------- Task Assignment Tests --------------------------- #

def test_set_task_valid(sample_node):
    """Test that set_task assigns valid tasks."""
    sample_node.supported_tasks = ["task1", "task2"]
    sample_node.set_task("task1")

    assert sample_node.task == "task1"


def test_set_task_invalid(sample_node):
    """Test that set_task raises an exception for unsupported tasks."""
    sample_node.supported_tasks = ["task1"]

    with pytest.raises(ValueError, match="Task 'task2' is not supported by Node TestNode."):
        sample_node.set_task("task2")


# --------------------------- Priority Handling Tests --------------------------- #

@pytest.mark.parametrize(
    "priority, expected_result",
    [(10, 10), (1, 1)],
)
def test_set_priority_valid(sample_node, priority, expected_result):
    """Test that set_priority accepts valid priorities."""
    sample_node.set_priority(priority)
    assert sample_node.priority == expected_result


@pytest.mark.parametrize(
    "priority, expected_exception",
    [(-1, ValueError), (0, ValueError)],
)
def test_set_priority_invalid(sample_node, priority, expected_exception):
    """Test that set_priority raises exceptions for invalid priorities."""
    with pytest.raises(expected_exception, match="Priority must be greater than or equal to 1."):
        sample_node.set_priority(priority)


# --------------------------- Status Update Tests --------------------------- #

def test_update_status(sample_node):
    """Test that the node updates its status based on the state."""
    sample_node.state_machine.current_state = MagicMock()
    sample_node.state_machine.current_state.name = "waiting"
    sample_node.dependencies = []

    sample_node.update_status()

    assert sample_node.status == "waiting for task"
