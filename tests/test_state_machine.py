import pytest
from unittest.mock import MagicMock
from src.shared.StateMachine import StateMachine
from src.shared.State import WaitingState, ReadyState, ProcessingState, ErrorState, InactiveState

# --------------------------- Fixtures --------------------------- #

@pytest.fixture
def mock_node():
    """Fixture to provide a mock node instance."""
    node = MagicMock(name="MockNode")
    node.dependencies = []
    node.task = None
    return node

@pytest.fixture
def state_machine(mock_node):
    """Fixture to provide a StateMachine instance."""
    return StateMachine(mock_node)

# --------------------------- StateMachine Initialization Tests --------------------------- #

def test_initial_state_is_ready(state_machine):
    """Test that the initial state is 'ready' when there are no dependencies and no task."""
    assert state_machine.current_state.name == "ready"

def test_initial_state_is_waiting_with_dependencies(mock_node):
    """Test that the initial state is 'waiting' when dependencies exist."""
    mock_node.dependencies = ["dep1", "dep2"]
    sm = StateMachine(mock_node)
    assert sm.current_state.name == "waiting"

# --------------------------- State Transitions --------------------------- #

def test_valid_state_transitions(state_machine):
    """Test valid state transitions."""
    valid_states = ["waiting", "ready", "processing", "error", "inactive"]

    for state in valid_states:
        state_machine.set_state(state)
        assert state_machine.current_state.name == state

def test_invalid_state_transitions(state_machine):
    """Test that invalid state transitions raise an exception."""
    state_machine.set_state("error")

    with pytest.raises(ValueError, match="Invalid state transition"):
        state_machine.set_state("processing")  # Invalid transition from error to processing

# --------------------------- State Logic Tests --------------------------- #

def test_handle_task_in_ready_state(state_machine, mock_node):
    """Test handle_task behavior in the 'ready' state."""
    state_machine.set_state("ready")
    mock_node.task = "Sample Task"

    result = state_machine.current_state.handle_task()

    # Assertions
    mock_node.process_task.assert_called_once()
    assert result["status"] == "success"

def test_handle_task_in_waiting_state(state_machine, mock_node):
    """Test handle_task behavior in the 'waiting' state."""
    state_machine.set_state("waiting")
    mock_node.check_dependency.return_value = False

    result = state_machine.current_state.handle_task()

    # Assertions
    assert result["status"] == "waiting"
    assert "Dependencies are unresolved" in result["message"]

def test_handle_task_in_processing_state(state_machine, mock_node):
    """Test handle_task behavior in the 'processing' state."""
    state_machine.set_state("processing")
    mock_node.task = "Sample Task"

    result = state_machine.current_state.handle_task()

    # Assertions
    mock_node.process_task.assert_called_once()
    assert result["status"] == "success"

def test_handle_task_in_error_state(state_machine):
    """Test handle_task behavior in the 'error' state."""
    state_machine.set_state("error")
    result = state_machine.current_state.handle_task()

    # Assertions
    assert result["status"] == "error"
    assert "Task processing not allowed" in result["message"]

def test_handle_task_in_inactive_state(state_machine):
    """Test handle_task behavior in the 'inactive' state."""
    state_machine.set_state("inactive")
    result = state_machine.current_state.handle_task()

    # Assertions
    assert result["status"] == "inactive"
    assert "Task processing is not allowed" in result["message"]

# --------------------------- Dependency Management Tests --------------------------- #

def test_unresolved_dependencies_keep_state_waiting(mock_node):
    """Test that unresolved dependencies keep the state in 'waiting'."""
    mock_node.dependencies = ["dep1"]
    mock_node.check_dependency.side_effect = lambda dep: dep != "dep1"  # "dep1" is unresolved

    sm = StateMachine(mock_node)
    sm.update_state()
    assert sm.current_state.name == "waiting"

def test_resolved_dependencies_update_state_to_ready(mock_node):
    """Test that resolving all dependencies updates the state to 'ready'."""
    mock_node.dependencies = ["dep1", "dep2"]
    mock_node.check_dependency.return_value = True

    sm = StateMachine(mock_node)
    sm.update_state()
    assert sm.current_state.name == "ready"

# --------------------------- StateMachine Error Handling --------------------------- #

def test_resolve_error_transitions_to_waiting(state_machine, mock_node):
    """Test that resolve_error transitions to 'waiting' after error resolution."""
    state_machine.set_state("error")
    mock_node.clear_error = MagicMock()

    state_machine.resolve_error()

    # Assertions
    mock_node.clear_error.assert_called_once()
    assert state_machine.current_state.name == "waiting"

def test_resolve_error_no_transition_if_not_in_error(state_machine):
    """Test that resolve_error does nothing if not in 'error' state."""
    state_machine.set_state("ready")
    state_machine.resolve_error()

    # Assertions
    assert state_machine.current_state.name == "ready"
