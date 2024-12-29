import pytest
from src.shared.GPTNode import GPTNode
from src.shared.AI_Node import AI_Node
from src.shared.Orchestrator import Orchestrator
from unittest.mock import patch

# --------------------------- Fixtures --------------------------- #

@pytest.fixture
def orchestrator():
    """Fixture to provide an Orchestrator instance."""
    return Orchestrator()


@pytest.fixture
def frontend_node():
    """Fixture to provide a sample frontend AI_Node."""
    return AI_Node(
        in_name="FrontendCoderNode",
        in_node_id="frontend1",
        in_description="Handles frontend coding tasks.",
        in_priority=1,
        in_status="active",
        in_purpose="Frontend Development",
        in_supported_tasks=["UI design"],
    )


@pytest.fixture
def security_node():
    """Fixture to provide a sample security AI_Node."""
    return AI_Node(
        in_name="SecurityNode",
        in_node_id="security1",
        in_description="Handles cybersecurity tasks.",
        in_priority=1,
        in_status="active",
        in_purpose="Cybersecurity",
        in_supported_tasks=["security analysis"],
    )


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
    assert responses["security1"]["status"] == "success"

    # Verify activity logs
    assert len(orchestrator.activity_logs) == 4  # 2 tasks assigned + 2 responses collected


# --------------------------- Task Assignment Validation Tests --------------------------- #

def test_set_task_rejects_unsupported_tasks():
    """
    Test that set_task raises an exception for unsupported tasks.
    """
    # Create a node that supports only "UI design"
    node = AI_Node(
        in_name="TestNode",
        in_node_id="test123",
        in_description="Sample Node for Tests",
        in_priority=1,
        in_status="active",
        in_purpose="Testing",
        in_supported_tasks=["UI design"],
    )

    # Test unsupported task assignment
    with pytest.raises(ValueError, match="Task 'Backend Development' is not supported"):
        node.set_task("Backend Development")

    # Test supported task assignment
    node.set_task("UI design")
    assert node.task == "UI design"
