from tasks.progress_estimation import (
    initialize_progress_bar,
    finalize_progress_bar,
    progress_estimation_node,
)
from shared.state import state
from shared.parallel_execution import execute_tasks
from logger_manager import (
    configure_logging,
    logger,
    log_event,
    log_error,
    log_task_event,
    configure_logger,
)


def main():
    """
    Main entry point for running the node network program.
    Configures standard logging behaviour, initializes progress bar, executes tasks, and finalizes progress.
    """
    configure_logging()
    initialize_progress_bar()

    try:
        # Execute tasks in parallel
        execute_tasks()
        # Show final progress estimation
        progress_estimation_node()
    finally:
        # Finalize the progress bar
        finalize_progress_bar()
        print("Workflow completed successfully!")


if __name__ == "__main__":
    # Initialize state
    state["total_tasks"] = len(state["nodes"])
    main()
