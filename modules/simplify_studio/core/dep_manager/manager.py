import logging
import os
import subprocess
from pathlib import Path
from typing import Dict

from blib2to3.pgen2.driver import Logger

from modules.simplify_studio.core.config.loader import Dependency


class DependencyManager:
    """
    Manages project dependencies, including cloning Git repositories.
    """

    def __init__(self, project_path: str, dependencies: Dict[str, "Dependency"]):
        """
        Initialize the DependencyManager.

        :param project_path: Path to the project directory.
        :param dependencies: Dependencies configuration.
        """
        self.project_path = Path(project_path).absolute()
        self.dependencies = dependencies
        self.logger = logging.getLogger(__name__)

    def install_dependencies(self) -> None:
        """
        Install all dependencies specified in the configuration.
        """
        for component_name, dependency in self.dependencies.items():
            git_url = dependency.git  # Directly access the 'git' attribute
            dependency_folder = dependency.dependency_folder  # Use the specified dependency folder
            if git_url and dependency_folder:
                self._clone_repository(git_url, dependency_folder)

    def _clone_repository(self, git_url: str, folder_name: str) -> None:
        """
        Clone a git repository to the specified folder.

        :param  git_url: The URL of the git repository.
        :param  folder_name: The name of the folder to clone into.
        """
        component_path = self.project_path / folder_name
        if component_path.exists() and any(component_path.iterdir()):
            self.logger.info(f"Directory {component_path} already exists. Skipping clone.")
            return

        os.makedirs(component_path, exist_ok=True)
        try:
            subprocess.run(["git", "clone", git_url, str(component_path)], check=True)
            self.logger.info(f"Cloned {git_url} into {component_path}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to clone {git_url}: {e}")
