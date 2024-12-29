from src.shared.utils import get_current_timestamp


class Orchestrator:
    def __init__(self):
        self.nodes = {}
        self.activity_logs = []

    def register_node(self, node):
        """Register a node in the orchestrator."""
        self.nodes[node.node_id] = node

    def assign_task(self, node_id, task):
        """Assign a task to a node."""
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not registered.")
        node = self.nodes[node_id]
        node.set_task(task)
        self.log_activity(f"Task assigned to {node_id}: {task}")

    def collect_responses(self):
        """Collect responses from all nodes."""
        responses = {}
        for node_id, node in self.nodes.items():
            if node.task:
                response = node.process_task()
                responses[node_id] = response
                self.log_activity(f"Response from {node_id}: {response}")
        return responses

    def log_activity(self, activity):
        """Log an orchestrator-level activity."""
        timestamp = get_current_timestamp()
        self.activity_logs.append({"activity": activity, "timestamp": timestamp})
