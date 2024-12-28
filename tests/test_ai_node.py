import pytest
import uuid
from shared.logger_utils import configure_logger, log_event, log_error, log_task_event, log_node_event
from shared.AI_Node import AI_Node

@pytest.fixture
def sample_node():
    """
    Fixture to create a sample AI_Node for testing.
    """
    return AI_Node(
        in_name="TestNode",
        in_node_id=None,
        in_description="This is a test node.",
        in_priority=1,
        in_status="active",
        in_purpose="Test",
        in_task="Initial Task"
    )


def test_node_initialization_with_uuid():
    """
    Test that the node initializes correctly with a generated UUID if no node_id is provided.
    """
    node = AI_Node(
        in_name="Node1",
        in_node_id=None,  # No node ID provided
        in_description="Test description",
        in_priority=5,
        in_status="active",
        in_purpose="Testing",
        in_task="Test Task"
    )
    assert node.node_id is not None
    assert isinstance(uuid.UUID(node.node_id), uuid.UUID)  # Validate the generated UUID
    assert node.status == "active"
    assert node.priority == 5


def test_node_initialization_with_provided_id():
    """
    Test that the node uses a provided ID instead of generating a new UUID.
    """
    provided_id = "12345"
    node = AI_Node(
        in_name="Node1",
        in_node_id=provided_id,
        in_description="Test description",
        in_priority=2,
        in_status="inactive",
        in_purpose="Testing",
        in_task="Test Task"
    )
    assert node.node_id == provided_id
    assert node.status == "inactive"
    assert node.priority == 2


def test_get_details(sample_node):
    """
    Test that the get_details method returns the correct details.
    """
    details = sample_node.get_details()
    assert details["node_id"] == sample_node.node_id
    assert details["description"] == sample_node.description
    assert details["priority"] == sample_node.priority
    assert details["status"] == sample_node.status
    assert details["purpose"] == sample_node.purpose
    assert details["task"] == sample_node.task


def test_set_status(sample_node):
    """
    Test that the set_status method updates the status correctly.
    """
    sample_node.set_status("inactive")
    assert sample_node.status == "inactive"


def test_str_representation(sample_node):
    """
    Test the string representation of the node.
    """
    result = str(sample_node)
    assert f"Node({sample_node.node_id}" in result
    assert f"Priority={sample_node.priority}" in result
    assert f"Status={sample_node.status}" in result
    assert f"Purpose={sample_node.purpose}" in result
    assert f"Task={sample_node.task}" in result


def test_set_task(sample_node):
    """
    Test that the set_task method updates the task correctly.
    """
    new_task = "Updated Task"
    sample_node.set_task(new_task)
    assert sample_node.task == new_task


def test_edge_case_empty_description():
    """
    Test that the node handles an empty description.
    """
    node = AI_Node(
        in_name="EdgeNode",
        in_node_id=None,
        in_description="",
        in_priority=1,
        in_status="active",
        in_purpose="Edge Test",
        in_task="Test Task"
    )
    assert node.description == ""


def test_edge_case_invalid_priority():
    """
    Test that the node handles an invalid priority (e.g., negative numbers).
    """
    with pytest.raises(ValueError):
        AI_Node(
            in_name="InvalidNode",
            in_node_id=None,
            in_description="Test description",
            in_priority=-5,  # Invalid priority
            in_status="active",
            in_purpose="Testing",
            in_task="Test Task"
        )


def test_edge_case_null_task():
    """
    Test that the node handles a None task.
    """
    node = AI_Node(
        in_name="EdgeNode",
        in_node_id=None,
        in_description="Test description",
        in_priority=1,
        in_status="active",
        in_purpose="Testing",
        in_task=None  # Null task
    )
    assert node.task is None
