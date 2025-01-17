from typing import Dict, Optional, TYPE_CHECKING
from src.shared.logger_manager import LoggerMixin

if TYPE_CHECKING:
    from src.shared.AI_Node import AI_Node


class NodeRegistry(LoggerMixin):
    def __init__(self):
        """
        Initialize the NodeRegistry.
        """
        self.nodes: Dict[str, "AI_Node"] = (
            {}
        )  # Properly annotate the type of the nodes dictionary

        super().__init__()  # Initialize loggers

    def register_node(self, node: "AI_Node") -> None:
        """
        Register a node in the registry.
        """
        self.nodes[node.node_id] = node
        self.log_debugger(f"Registered Node: {node.node_id} ({node.name})")

    def deregister_node(self, node_id: str) -> None:
        """
        Remove a node from the registry by its ID.
        """
        if node_id in self.nodes:
            del self.nodes[node_id]
            self.log_debugger(f"Deregistered Node: {node_id}")

    def get_node_by_id(self, node_id: str) -> Optional["AI_Node"]:
        """
        Retrieve a node by its ID. Returns None if the node is not found.
        """
        return self.nodes.get(node_id)

    def get_all_nodes(self) -> Dict[str, "AI_Node"]:
        """
        Get all nodes in the registry.
        """
        return self.nodes

    def debug_registry(self) -> None:
        """
        Print all nodes in the registry for debugging purposes.
        """
        for node_id, node in self.nodes.items():
            self.log_debugger(
                f"Node ID: {node_id}, Node Name: {node.name}, Status: {node.status}"
            )
