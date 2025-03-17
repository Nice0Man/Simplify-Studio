import os
from pathlib import Path
from typing import Optional, Dict

import yaml

from modules.simplify_studio.core.dep_manager.manager import DependencyManager


class ProjectBuilder:
    """
    Builder class for creating and managing CMake C/C++ projects.

    This class provides a step-by-step approach to configure and create a project,
    including directory structure setup, CMake configuration, dependency management,
    and build system generation.
    """

    def __init__(self):
        """
        Initialize a new ProjectBuilder instance with default settings.
        """
        self.project_name = None
        self.project_path = None
        self.config = {}
        self.structure_template = {}
        self.dependency_manager = None

    def set_project_name(self, project_name: str) -> "ProjectBuilder":
        """
        Set the project name.

        Args:
            project_name: Name of the C/C++ project.

        Returns:
            ProjectBuilder: The current instance for method chaining.
        """
        self.project_name = project_name
        return self

    def set_project_path(self, project_path: str) -> "ProjectBuilder":
        """
        Set the project path.

        Args:
            project_path: Root directory where the project will be created.

        Returns:
            ProjectBuilder: The current instance for method chaining.
        """
        self.project_path = Path(project_path).absolute()
        return self

    def set_config(self, config: Optional[Dict] = None) -> "ProjectBuilder":
        """
        Set the project configuration.

        Args:
            config: Optional configuration dictionary with project settings.

        Returns:
            ProjectBuilder: The current instance for method chaining.
        """
        self.config = config or {}
        return self

    def load_structure_template(
        self, template_file: Optional[str] = None
    ) -> "ProjectBuilder":
        """
        Load the project structure template from a YAML file or use a default template.

        Args:
            template_file: Path to a YAML file defining the project structure template.

        Returns:
            ProjectBuilder: The current instance for method chaining.
        """
        if template_file:
            with open(template_file, "r") as file:
                self.structure_template = yaml.safe_load(file)
            # Initialize DependencyManager with the template file
            self.dependency_manager = DependencyManager(
                self.project_path, template_file
            )
        else:
            self.structure_template = {
                "src": [],
                "include": [self.project_name],
                "tests": [],
                "build": [],
                "docs": [],
                "cmake": [],
            }
        return self

    def create_project_directory(self) -> None:
        """
        Create the main project directory.
        """
        os.makedirs(self.project_path, exist_ok=True)

    def create_subdirectories(self) -> None:
        """
        Create subdirectories based on the template.
        """
        for subdir, nested_dirs in self.structure_template.items():
            subdir_path = self.project_path / subdir
            os.makedirs(subdir_path, exist_ok=True)
            for nested_dir in nested_dirs:
                os.makedirs(subdir_path / nested_dir, exist_ok=True)

    def build(self) -> bool:
        """
        Finalize the project creation process.

        Returns:
            bool: True if project creation was successful, False otherwise.
        """
        try:
            self.create_project_directory()
            self.create_subdirectories()
            if self.dependency_manager:
                self.dependency_manager.install_dependencies()
            return True
        except Exception as e:
            print(f"Error creating project: {str(e)}")
            return False


def main():
    builder = ProjectBuilder()
    success = (
        builder.set_project_name("MyCMakeProject")
        .set_project_path("./my_cmake_project")
        .set_config({"CMAKE_CXX_STANDARD": "17", "ENABLE_TESTING": "ON"})
        .load_structure_template("project_structure.yaml")
        .build()
    )

    if success:
        print("Project created successfully.")
    else:
        print("Failed to create the project.")


if __name__ == "__main__":
    main()
