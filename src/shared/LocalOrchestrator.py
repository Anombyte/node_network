class LocalOrchestrator(Orchestrator):
    def __init__(self, team_name):
        super().__init__(name=f"Local Orchestrator: {team_name}")
        self.team_name = team_name
        self.nodes = {}  # Dictionary of nodes in this team

    def assign_task(self, task):
        """Distribute tasks to suitable nodes within the team."""
        suitable_node = self.find_suitable_node(task)
        if suitable_node:
            suitable_node.set_task(task)
            self.log_activity(f"Task '{task}' assigned to node {suitable_node.name}.")
        else:
            self.log_activity(f"No suitable node found for task: {task}.")

    def find_suitable_node(self, task):
        """Find a node capable of handling the task."""
        # Example logic: Return the first idle node that supports the task
        for node in self.nodes.values():
            if node.is_task_supported(task) and node.get_status() == "idle":
                return node
        return None

    def report_progress(self):
        """Collect progress updates from all nodes."""
        progress = {node_id: node.get_status() for node_id, node in self.nodes.items()}
        self.log_activity(f"Progress report: {progress}")
        return {"team_name": self.team_name, "progress": progress}

    def receive_data(self, data, from_team=None):
        """Handle incoming data from other teams."""
        self.update_context("received_data", data)
        if from_team:
            self.log_activity(f"Received data from team {from_team}: {data}")
