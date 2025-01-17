from src.shared.AI_Node import AI_Node
from src.shared.utils import get_current_timestamp


class GPTNode(AI_Node):
    def generate_task_prompt(self):
        """Generate a detailed GPT-specific task prompt."""
        if not self.task:
            raise ValueError("No task assigned to generate a task prompt.")
        return f"System: {self.identity_prompt.format(purpose=self.purpose)}\nTask: {self.task}"

    def process_task(self):
        """Process the task using the GPT API."""
        if not self.task:
            self.log_error(
                f"No task assigned to Node {self.name} (ID: {self.node_id})."
            )
            return {"status": "error", "message": "No task assigned."}

        try:
            prompt = self.generate_task_prompt()
            self.log_node_event(self.name, self.node_id, f"Generated prompt: {prompt}")

            # Simulate API call (replace with actual API integration)
            output = f"GPT response for: {self.task}"

            result = {
                "status": "success",
                "node_id": self.node_id,
                "task": self.task,
                "output": output,
                "timestamp": get_current_timestamp(),
            }
            self.log_activity(f"Processed task: {self.task}", result)
            return result

        except Exception as e:
            self.log_error(f"Error processing task in GPTNode {self.name}: {e}")
            return {"status": "error", "message": str(e)}
