import pytest
from src.shared.AI_Node import AI_Node
from src.shared.NodeRegistry import NodeRegistry
from src.shared.StateMachine import StateMachine

# --------------------------- Fixtures --------------------------- #


@pytest.fixture
def node_registry():
    """Fixture to initialize the NodeRegistry."""
    return NodeRegistry()


@pytest.fixture
def sample_node(node_registry):
    """Fixture for an AI_Node with real NodeRegistry and StateMachine."""
    return AI_Node(
        in_name="TestNode",
        in_node_id="node-123",
        in_description="Sample Node for Integration Test",
        in_priority=5,
        in_status="active",
        in_purpose="Testing",
        in_supported_tasks=["task1"],
        in_dependencies=[
            {"id": "dep1", "resolved": False},
            {"id": "dep2", "resolved": False},
        ],
        in_node_registry=node_registry,  # Pass the correct NodeRegistry instance
        in_state_machine=None,  # Automatically initialize with default StateMachine
    )


@pytest.fixture
def dependency_nodes(node_registry):
    """Fixture to create and register dependency nodes."""
    dep1 = AI_Node(
        in_name="Dependency1",
        in_node_id="dep1",
        in_description="Dependency Node 1",
        in_priority=3,
        in_status="idle",
        in_purpose="Dependency Resolution",
        in_supported_tasks=[],
        in_dependencies=[],
        in_node_registry=node_registry,
    )
    dep2 = AI_Node(
        in_name="Dependency2",
        in_node_id="dep2",
        in_description="Dependency Node 2",
        in_priority=2,
        in_status="idle",
        in_purpose="Dependency Resolution",
        in_supported_tasks=[],
        in_dependencies=[],
        in_node_registry=node_registry,
    )
    return dep1, dep2


# --------------------------- Test --------------------------- #


def test_integration_workflow(sample_node, dependency_nodes, node_registry):
    """
    Test the workflow: Assign task, resolve dependencies, and process the task.
    """
    # Register the dependencies
    dep1, dep2 = dependency_nodes
    assert node_registry.get_node_by_id("dep1") == dep1
    assert node_registry.get_node_by_id("dep2") == dep2

    # Assign a task to the sample node
    sample_node.set_task("task1")
    assert sample_node.task == "task1"
    assert sample_node.state_machine.current_state.name == "waiting"

    # Resolve dependencies
    dep1.state_machine.set_state("ready")  # Simulate dependency being ready
    dep2.state_machine.set_state("ready")
    assert dep1.state_machine.current_state.name == "ready"
    assert dep2.state_machine.current_state.name == "ready"

    # Process the task
    result = sample_node.process_task()
    assert result["status"] == "success"
    assert result["task"] == "task1"
    assert result["output"] == "Generated output for task: task1"
    assert "timestamp" in result

    # Verify state transitions
    assert sample_node.state_machine.current_state.name == "ready"
