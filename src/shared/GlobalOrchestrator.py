class GlobalOrchestrator(Orchestrator):
    def __init__(self, name="Global Orchestrator"):
        super().__init__(name)
        self.teams = {}  # Dictionary to track team orchestrators

    def assign_high_level_goal(self, goal_description):
        """Break down the global goal and distribute tasks to team orchestrators."""
        self.log_activity(f"Assigning goal: {goal_description}")
        tasks = self.break_down_goal(goal_description)
        for team_name, task in tasks.items():
            if team_name in self.teams:
                self.teams[team_name].assign_task(task)
            else:
                self.log_activity(f"Team {team_name} not found!")

    def break_down_goal(self, goal_description):
        """Break a goal into smaller tasks (dummy implementation for now)."""
        # Example: Convert goal into a dict of team-specific tasks
        return {
            "Team_A": "Design website layout",
            "Team_B": "Write website content",
        }

    def collect_team_updates(self):
        """Aggregate progress from all team orchestrators."""
        for team_name, orchestrator in self.teams.items():
            updates = orchestrator.report_progress()
            self.update_context(team_name, updates)

    def mediate_team_interaction(self, source_team, target_team, data):
        """Facilitate communication between teams via the orchestrator."""
        if target_team in self.teams:
            self.teams[target_team].receive_data(data, from_team=source_team)
        else:
            self.log_activity(f"Target team {target_team} not found.")
