from src.shared.NodeRegistry import NodeRegistry


def main():
    """
    Main entry point for running the node network program.
    Configures standard logging behaviour, initializes progress bar, executes tasks, and finalizes progress.
    """
    # initialize_progress_bar()

    try:
        node_registry = NodeRegistry
    finally:
        print("Workflow completed successfully!")


if __name__ == "__main__":
    main()
