from shared import state
from logger_manager import logger, log_event, log_error, log_task_event

name = ""
node_name = ""
node_target = ""


class task:
    def __init__(self, in_name, in_node_name):
        self.name = in_name
        self.node_name = in_node_name
        log_task_event(name, f"Created task: {name}")


def task(input_text, node_name):
    """
    Summarizer GPT function.
    """
    logger.info(f"{node_name}: Task execution started.")
    summary = (
        f"Summary of: {input_text}"  # Replace with actual GPT summarization logic.
    )
    state["nodes"][node_name]["output"] = summary
    state["nodes"][node_name]["status"] = "Completed"
    logger.info(f"{node_name}: Task completed with output: {summary}")
