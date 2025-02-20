from src.shared.utils import get_current_timestamp


class Orchestrator:
    def __init__(self):
        self.nodes = {}
        self.activity_logs = []  # Shared Logging Mechanism
        self.context = {}  # Shared attribute for managing context

    def register_node(self, node):
        """
        Register a node in the orchestrator.
        """
        self.nodes[node.node_id] = node
        self.log_activity(f"Registered node: {node.node_id} ({node.name})")

    def assign_task(self, node_id, task):
        """
        Assign a task to a node and update its state.
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not registered.")

        node = self.nodes[node_id]
        node.set_task(task)
        node.update_state()  # Ensure the state reflects the assigned task
        self.log_activity(f"Task assigned to {node_id}: {task}")

    def check_node_states(self):
        """
        Check the current state of all nodes and log their status.
        """
        for node_id, node in self.nodes.items():
            state = node.state_machine.get_state()
            self.log_activity(f"Node {node_id} is in state: {state.name}")

    def collect_responses(self):
        """
        Collect responses from all nodes and update their states accordingly.
        """
        responses = {}
        for node_id, node in self.nodes.items():
            if node.task:
                response = node.process_task()
                responses[node_id] = response
                node.update_state()  # Reflect state changes after processing
                self.log_activity(f"Response from {node_id}: {response}")
        return responses

    def log_activity(self, activity):
        """
        Log an orchestrator-level activity.
        """
        timestamp = get_current_timestamp()
        self.activity_logs.append({"activity": activity, "timestamp": timestamp})

    def get_context(self):
        """Retrieve the orchestrator's current context."""
        return self.context

    def update_context(self, key, value):
        """Update a specific part of the context."""
        self.context[key] = value
