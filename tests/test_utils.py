import pytest
from shared.utils import (
    validate_node_config,
    validate_message,
    retry_operation,
    fallback_on_error,
)

# =======================
# Test: Validation Utilities
# =======================


def test_validate_node_config_valid():
    """Test validate_node_config with valid config."""
    valid_config = {"name": "test_node", "type": "worker", "node_id": "1234"}
    # Should not raise an exception
    validate_node_config(valid_config)


def test_validate_node_config_invalid():
    """Test validate_node_config raises ValueError for missing keys."""
    invalid_config = {"name": "test_node", "type": "worker"}  # Missing "node_id"
    with pytest.raises(ValueError, match="Missing required key: node_id"):
        validate_node_config(invalid_config)


def test_validate_message_valid():
    """Test validate_message with a valid message."""
    valid_message = {"sender": "node1", "receiver": "node2", "content": "Hello!"}
    # Should not raise an exception
    validate_message(valid_message)


def test_validate_message_invalid():
    """Test validate_message raises ValueError for missing keys."""
    invalid_message = {"sender": "node1", "content": "Hello!"}  # Missing "receiver"
    with pytest.raises(ValueError, match="Message is missing key: receiver"):
        validate_message(invalid_message)


# =======================
# Test: Decorators
# =======================


def test_retry_operation_success():
    """Test retry_operation succeeds on the first attempt."""

    @retry_operation(retry_count=3)
    def success_function():
        return "Success!"

    assert success_function() == "Success!"


def test_retry_operation_failure():
    """Test retry_operation raises an exception after retries."""
    attempts = 0

    @retry_operation(retry_count=3)
    def fail_function():
        nonlocal attempts
        attempts += 1
        raise ValueError("Intentional Failure")

    with pytest.raises(ValueError, match="Intentional Failure"):
        fail_function()

    assert attempts == 3  # Ensure it retries the correct number of times


def test_fallback_on_error():
    """Test fallback_on_error executes fallback logic."""

    def fallback_func():
        return "Fallback Success!"

    @fallback_on_error(fallback_func)
    def fail_function():
        raise ValueError("Intentional Failure")

    assert fail_function() == "Fallback Success!"
