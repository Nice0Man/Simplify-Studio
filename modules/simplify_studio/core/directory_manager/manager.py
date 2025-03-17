import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class DirectoryNode:
    name: str
    description: str = ""
    subdirectories: List["DirectoryNode"] = field(default_factory=list)

    logger = logging.getLogger(__name__)

    def create_directories(self, base_path: Path) -> None:
        """
        Create this directory and its subdirectories.

        :param base_path: The base path where this directory should be created.
        :return: None
        """
        dir_path = base_path / self.name
        if dir_path.exists():
            self.logger.info(f"Directory already exists: {dir_path}")
        else:
            os.makedirs(dir_path, exist_ok=True)
            self.logger.info(f"Created directory {dir_path}")

        for subdirectory in self.subdirectories:
            subdirectory.create_directories(dir_path)

    def add_subdirectory(self, node: "DirectoryNode") -> None:
        """
        Add a subdirectory to this directory node.

        :param node: The subdirectory node to add.
        :return: None
        """
        self.subdirectories.append(node)

    def __iter__(self):
        """
        Return an iterator over the subdirectories.

        :return: Iterator[DirectoryNode] - An iterator over the subdirectories.
        """
        return iter(self.subdirectories)

    def __str__(self) -> str:
        """
        Return a string representation of the directory tree.

        :return: str - A tree-like string representation of the directory structure.
        """
        return self._tree_representation()

    def _tree_representation(
        self, is_last: bool = True, depth: int = 0, parent_prefix: str = ""
    ) -> str:
        """
        Generate a tree-like string representation of the directory structure.

        :param is_last: Is the node last in the list of subsidiaries of the parent.
        :param depth: Current depth in a tree (for root = 0).
        :param parent_prefix: Prefix for inheritance of indentation from the parent.
        :return: str - A string representation of the node and its subdirectories.
        """
        current_prefix = ""
        child_prefix = ""

        if depth > 0:
            current_prefix = parent_prefix + ("└── " if is_last else "├── ")
            child_prefix = parent_prefix + ("    " if is_last else "│   ")

        result = f"{current_prefix}{self.name}"
        if self.description and depth == 0:
            result += f": {self.description}"
        result += "\n"

        for i, child in enumerate(self.subdirectories):
            is_last_child = i == len(self.subdirectories) - 1
            result += child._tree_representation(
                is_last=is_last_child, depth=depth + 1, parent_prefix=child_prefix
            )

        return result


class DirectoryManager:
    """
    Manages the creation of project directories.
    """

    def __init__(self, path: str, structure: Dict[str, DirectoryNode]):
        """
        Initialize the DirectoryManager.

        :param path: Path to the project directory.
        :param structure: Directory structure configuration.
        :return: None
        """
        self.project_path = Path(path).absolute()
        self.structure = structure

    def create_directories(self) -> None:
        """
        Create directories based on the structure configuration.

        :return: None
        """
        self.project_path.mkdir(parents=True, exist_ok=True)
        for node in self.structure.values():  # type: DirectoryNode
            node.create_directories(self.project_path)
