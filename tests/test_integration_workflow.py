import pytest
from unittest.mock import MagicMock, patch
from src.shared.Orchestrator import Orchestrator
from src.shared.AI_Node import AI_Node

# --------------------------- Fixtures --------------------------- #

@pytest.fixture
def orchestrator():
    """Fixture to provide an Orchestrator instance."""
    return Orchestrator()

@pytest.fixture
def frontend_node():
    """Fixture to provide a sample frontend AI_Node."""
    node = AI_Node(
        in_name="FrontendCoderNode",
        in_node_id="frontend1",
        in_description="Handles frontend coding tasks.",
        in_priority=1,
        in_status="active",
        in_purpose="Frontend Development",
        in_supported_tasks=["UI design"],
    )
    node.process_task = MagicMock(return_value={"status": "success", "output": "Frontend processed"})
    return node

@pytest.fixture
def backend_node():
    """Fixture to provide a sample backend AI_Node."""
    node = AI_Node(
        in_name="BackendCoderNode",
        in_node_id="backend1",
        in_description="Handles backend coding tasks.",
        in_priority=1,
        in_status="active",
        in_purpose="Backend Development",
        in_supported_tasks=["API development"],
    )
    node.process_task = MagicMock(return_value={"status": "success", "output": "Backend processed"})
    return node

@pytest.fixture
def security_node():
    """Fixture to provide a sample security AI_Node."""
    node = AI_Node(
        in_name="SecurityNode",
        in_node_id="security1",
        in_description="Handles cybersecurity tasks.",
        in_priority=1,
        in_status="active",
        in_purpose="Cybersecurity",
        in_supported_tasks=["security analysis"],
    )
    node.process_task = MagicMock(return_value={"status": "success", "output": "Security processed"})
    return node

# --------------------------- Integration Workflow Tests --------------------------- #

def test_integration_workflow(orchestrator, frontend_node, security_node):
    """
    Test the full integration workflow:
    - Register nodes
    - Assign tasks
    - Collect responses
    - Verify activity logs
    """
    # Register nodes
    orchestrator.register_node(frontend_node)
    orchestrator.register_node(security_node)

    # Assign tasks
    orchestrator.assign_task("frontend1", "UI design")
    orchestrator.assign_task("security1", "security analysis")

    # Collect responses
    responses = orchestrator.collect_responses()

    # Assertions
    assert "frontend1" in responses
    assert "security1" in responses
    assert responses["frontend1"]["status"] == "success"
    assert responses["frontend1"]["output"] == "Frontend processed"
    assert responses["security1"]["status"] == "success"
    assert responses["security1"]["output"] == "Security processed"

    # Verify activity logs
    assert len(orchestrator.activity_logs) == 4  # 2 tasks assigned + 2 responses collected

def test_task_assignment_with_unsupported_task(orchestrator, frontend_node):
    """
    Test that the orchestrator raises an error when assigning an unsupported task.
    """
    orchestrator.register_node(frontend_node)

    with pytest.raises(ValueError, match="Task 'Backend Development' is not supported"):
        orchestrator.assign_task("frontend1", "Backend Development")

def test_responses_with_mocked_nodes(orchestrator):
    """
    Test response collection from mocked nodes.
    """
    mock_node = MagicMock()
    mock_node.node_id = "mock1"
    mock_node.process_task.return_value = {"status": "success", "output": "Mock output"}
    orchestrator.register_node(mock_node)

    orchestrator.assign_task("mock1", "Mock task")
    responses = orchestrator.collect_responses()

    # Assertions
    mock_node.process_task.assert_called_once()
    assert responses["mock1"]["status"] == "success"
    assert responses["mock1"]["output"] == "Mock output"

def test_orchestrator_activity_logging(orchestrator, frontend_node):
    """
    Test that orchestrator logs all activity correctly.
    """
    orchestrator.register_node(frontend_node)
    orchestrator.assign_task("frontend1", "UI design")
    responses = orchestrator.collect_responses()

    # Assertions
    assert len(orchestrator.activity_logs) == 2  # 1 task assigned + 1 response collected
    assert orchestrator.activity_logs[0]["activity"] == "Task assigned to frontend1: UI design"
    assert "Response from frontend1" in orchestrator.activity_logs[1]["activity"]

def test_registering_duplicate_node(orchestrator, frontend_node):
    """
    Test that registering a node with an existing ID replaces the old node.
    """
    orchestrator.register_node(frontend_node)

    # Register another node with the same ID
    duplicate_node = MagicMock()
    duplicate_node.node_id = "frontend1"
    orchestrator.register_node(duplicate_node)

    # Assertions
    assert orchestrator.nodes["frontend1"] == duplicate_node

def test_unregistered_node_task_assignment(orchestrator):
    """
    Test that assigning a task to an unregistered node raises an error.
    """
    with pytest.raises(ValueError, match="Node unregistered1 not registered."):
        orchestrator.assign_task("unregistered1", "Some task")

def test_task_reassignment(orchestrator, frontend_node):
    """
    Test that reassigning a task to a node overwrites the previous task.
    """
    orchestrator.register_node(frontend_node)
    orchestrator.assign_task("frontend1", "UI design")
    orchestrator.assign_task("frontend1", "UI redesign")  # Reassign a new task

    # Collect responses
    responses = orchestrator.collect_responses()

    # Assertions
    assert responses["frontend1"]["task"] == "UI redesign"
