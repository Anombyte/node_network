import pytest
from unittest.mock import MagicMock, patch
from src.shared.AI_Node import AI_Node
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
        in_supported_tasks=["task1", "task2"],
        in_dependencies=[],  # Start with no dependencies
    )


@pytest.fixture
def dependent_node():
    """Fixture to provide an AI_Node with dependencies."""
    return AI_Node(
        in_name="DependentNode",
        in_node_id="dep1",
        in_description="Node with dependencies",
        in_priority=1,
        in_status="active",
        in_purpose="Dependency Testing",
        in_dependencies=["dep1", "dep2"],
    )


# --------------------------- State Initialization Tests --------------------------- #

def test_initial_state_waiting_with_dependencies(dependent_node):
    """Test that the initial state is 'waiting' if dependencies exist."""
    assert dependent_node.state_machine.current_state.name == "waiting"


def test_initial_state_ready_without_dependencies(sample_node):
    """Test that the initial state is 'ready' when there are no dependencies."""
    assert sample_node.state_machine.current_state.name == "ready"


# --------------------------- State Transition Tests --------------------------- #

def test_state_transitions_to_processing_on_task_assignment(sample_node):
    """Test that the node transitions to 'processing' when a task is assigned."""
    sample_node.set_task("task1")
    sample_node.state_machine.update_state()
    assert sample_node.state_machine.current_state.name == "processing"


def test_state_remains_waiting_with_unresolved_dependencies(dependent_node):
    """Test that the node remains in 'waiting' state if dependencies are unresolved."""
    dependent_node.state_machine.update_state()
    assert dependent_node.state_machine.current_state.name == "waiting"


def test_resolve_dependencies_transitions_to_ready(dependent_node):
    """Test that resolving dependencies transitions the state to 'ready'."""
    dependent_node.resolve_dependency("dep1")
    dependent_node.resolve_dependency("dep2")
    dependent_node.state_machine.update_state()
    assert dependent_node.state_machine.current_state.name == "ready"


def test_state_machine_invalid_transition(dependent_node):
    """Test that invalid state transitions raise an exception."""
    dependent_node.state_machine.set_state("error")
    with pytest.raises(ValueError, match="Invalid state transition"):
        dependent_node.state_machine.set_state("processing")  # Invalid transition from error to processing


def test_state_machine_allows_valid_transitions(sample_node):
    """Test that valid state transitions are allowed."""
    sample_node.state_machine.set_state("ready")
    sample_node.state_machine.set_state("processing")
    sample_node.state_machine.set_state("error")
    sample_node.state_machine.set_state("inactive")  # Valid transitions should not raise exceptions


# --------------------------- State Behavior Tests --------------------------- #

def test_waiting_state_does_not_process_task(dependent_node):
    """Test that tasks are not processed in the 'waiting' state."""
    result = dependent_node.state_machine.current_state.handle_task()
    assert result["status"] == "waiting"
    assert "Dependencies are unresolved" in result["message"]


def test_ready_state_transitions_to_processing_with_task(sample_node):
    """Test that the ready state transitions to 'processing' when a task is assigned."""
    sample_node.set_task("task1")
    result = sample_node.state_machine.current_state.handle_task()
    assert result["status"] == "success"
    assert result["task"] == "task1"


def test_ready_state_with_no_task(sample_node):
    """Test that the ready state transitions appropriately when no task is assigned."""
    sample_node.state_machine.update_state()
    result = sample_node.state_machine.current_state.handle_task()
    assert result["status"] == "no_task"
    assert "No task assigned" in result["message"]


def test_processing_state_executes_task(sample_node):
    """Test that the processing state executes the task."""
    sample_node.set_task("task1")
    sample_node.state_machine.set_state("processing")
    sample_node.process_task = MagicMock(return_value={"status": "success", "output": "Task completed"})

    result = sample_node.state_machine.current_state.handle_task()
    sample_node.process_task.assert_called_once()
    assert result["status"] == "success"
    assert result["output"] == "Task completed"


def test_error_state_blocks_task_processing(sample_node):
    """Test that tasks are not processed in the 'error' state."""
    sample_node.state_machine.set_state("error")
    result = sample_node.state_machine.current_state.handle_task()
    assert result["status"] == "error"
    assert "Task processing not allowed" in result["message"]


def test_inactive_state_blocks_task_processing(sample_node):
    """Test that tasks are not processed in the 'inactive' state."""
    sample_node.state_machine.set_state("inactive")
    result = sample_node.state_machine.current_state.handle_task()
    assert result["status"] == "inactive"
    assert "Task processing is not allowed" in result["message"]


# --------------------------- Dependency-Driven State Tests --------------------------- #

def test_unresolved_dependencies_keep_state_waiting(dependent_node):
    """Test that unresolved dependencies keep the state in 'waiting'."""
    dependent_node.resolve_dependency("dep1")
    dependent_node.state_machine.update_state()
    assert dependent_node.state_machine.current_state.name == "waiting"  # Still waiting due to dep2


def test_resolved_dependencies_trigger_state_update_to_ready(dependent_node):
    """Test that resolving all dependencies triggers state update to 'ready'."""
    dependent_node.resolve_dependency("dep1")
    dependent_node.resolve_dependency("dep2")
    dependent_node.state_machine.update_state()
    assert dependent_node.state_machine.current_state.name == "ready"


def test_dependency_resolution_during_waiting_state(dependent_node):
    """Test that resolving dependencies during 'waiting' state triggers the correct state transition."""
    dependent_node.state_machine.current_state.handle_task()  # Check unresolved dependencies
    dependent_node.resolve_dependency("dep1")
    dependent_node.resolve_dependency("dep2")
    dependent_node.state_machine.update_state()

    assert dependent_node.state_machine.current_state.name == "ready"
