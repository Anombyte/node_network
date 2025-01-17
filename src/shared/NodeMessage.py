from src.shared.utils import get_current_timestamp, get_unique_id


class NodeMessage:
    """
    Base class for all messages in the system.
    """

    def __init__(self, sender, recipient, message_id=None, timestamp=None):
        self.sender = sender
        self.recipient = recipient
        self.message_id = message_id or get_unique_id()
        self.timestamp = timestamp or get_current_timestamp()

    def to_dict(self):
        """Serialize the message to a dictionary for queueing or logging."""
        return {
            "message_id": self.message_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "type": self.__class__.__name__,
            "timestamp": self.timestamp,
            "payload": self.get_payload(),
        }

    def get_payload(self):
        """Override in subclasses to return specific payload data."""
        raise NotImplementedError("Subclasses must implement get_payload().")


class TaskMessage(NodeMessage):
    """
    Message for assigning tasks to nodes.
    """

    def __init__(
        self,
        sender,
        recipient,
        task_id,
        description,
        priority,
        deadline,
        dependencies=None,
    ):
        super().__init__(sender, recipient)
        self.task_id = task_id
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.dependencies = dependencies or []

    def get_payload(self):
        return {
            "task_id": self.task_id,
            "description": self.description,
            "priority": self.priority,
            "deadline": self.deadline,
            "dependencies": self.dependencies,
        }


class StatusUpdateMessage(NodeMessage):
    """
    Message for reporting progress or status updates.
    """

    def __init__(self, sender, recipient, task_id, status, progress, issues=None):
        super().__init__(sender, recipient)
        self.task_id = task_id
        self.status = status
        self.progress = progress
        self.issues = issues

    def get_payload(self):
        return {
            "task_id": self.task_id,
            "status": self.status,
            "progress": self.progress,
            "issues": self.issues,
        }


class DependencyRequestMessage(NodeMessage):
    """
    Message for requesting unresolved dependencies.
    """

    def __init__(self, sender, recipient, task_id, required_data):
        super().__init__(sender, recipient)
        self.task_id = task_id
        self.required_data = required_data

    def get_payload(self):
        return {
            "task_id": self.task_id,
            "required_data": self.required_data,
        }


class DependencyResponseMessage(NodeMessage):
    """
    Message for responding to dependency requests.
    """

    def __init__(self, sender, recipient, task_id, provided_data):
        super().__init__(sender, recipient)
        self.task_id = task_id
        self.provided_data = provided_data

    def get_payload(self):
        return {
            "task_id": self.task_id,
            "provided_data": self.provided_data,
        }
