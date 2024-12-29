import unittest
from unittest.mock import MagicMock
from logger_manager import Logger  # Mock the Logger
from shared.AI_Node import AI_Node  # Import the Node class


class TestNode(unittest.TestCase):

    def setUp(self):
        """
        Set up common test fixtures for the tests.
        """
        # Mock the Logger to avoid actual logging during tests
        Logger.log_node_event = MagicMock()

        # Common attributes for Node initialization
        self.name = "TestNode"
        self.node_id = "12345"
        self.description = "This is a test node."
        self.priority = 5
        self.status = "active"
        self.purpose = "testing"
        self.task = "test task"

        # Create a Node instance
        self.node = AI_Node(
            in_name=self.name,
            in_node_id=self.node_id,
            in_description=self.description,
            in_priority=self.priority,
            in_status=self.status,
            in_purpose=self.purpose,
            in_task=self.task,
        )

    def test_initialization(self):
        """
        Test that the Node is initialized with correct values.
        """
        self.assertEqual(self.node.name, self.name)
        self.assertEqual(self.node.node_id, self.node_id)
        self.assertEqual(self.node.description, self.description)
        self.assertEqual(self.node.priority, self.priority)
        self.assertEqual(self.node.status, self.status)
        self.assertEqual(self.node.purpose, self.purpose)
        self.assertEqual(self.node.task, self.task)

    def test_get_details(self):
        """
        Test the get_details method.
        """
        expected_details = {
            "node_id": self.node_id,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "purpose": self.purpose,
            "task": self.task,
        }
        self.assertEqual(self.node.get_details(), expected_details)

    def test_set_status(self):
        """
        Test the set_status method.
        """
        new_status = "inactive"
        self.node.set_status(new_status)

        # Check that the status is updated
        self.assertEqual(self.node.status, new_status)

        # Check that the logger was called with the correct message
        Logger.log_node_event.assert_called_with(
            self.name, f"Status updated to {new_status}"
        )

    def test_str_representation(self):
        """
        Test the __str__ method.
        """
        expected_str = f"Node({self.node_id}, Priority={self.priority}, Status={self.status}, Purpose={self.purpose}, Task={self.task})"
        self.assertEqual(str(self.node), expected_str)

    def test_logger_singleton(self):
        """
        Test that all instances of Logger share the same object.
        """
        logger1 = Logger()
        logger2 = Logger()

        # Assert both instances are the same
        self.assertIs(logger1, logger2)


if __name__ == "__main__":
    unittest.main()
