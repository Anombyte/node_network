from shared import state
from shared.logging import logger, log_event, log_error, log_task_event
    
name = ""
purpose = ""
    
class task:
    def __init__(self, in_name, in_purpose):
        self.name = in_name
        self.purpose = in_purpose
        log_task_event(name,f"Created node: {name} with the purpose {purpose}")
















def task(input_text, node_name):
    """
    Summarizer GPT function.
    """
    logger.info(f"{node_name}: Task execution started.")
    summary = f"Summary of: {input_text}"  # Replace with actual GPT summarization logic.
    state["nodes"][node_name]["output"] = summary
    state["nodes"][node_name]["status"] = "Completed"
    logger.info(f"{node_name}: Task completed with output: {summary}")


