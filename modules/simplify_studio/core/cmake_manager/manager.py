import logging
from pathlib import Path
from typing import Dict

from modules.simplify_studio.core.cmake_manager.builder import CMakeBuilder
from modules.simplify_studio.core.config.loader import (
    Metadata,
    CMakeSettings,
    Dependency,
    DirectoryNode,
)


class CMakeManager:
    """
    Manages CMake configuration and setup for the project.
    """

    def __init__(
        self,
        metadata: Metadata,
        cmake_settings: CMakeSettings,
        dependencies: Dict[str, Dependency],
        structure: Dict[str, DirectoryNode],
        project_path: str,
    ):
        """
        Initialize the CMakeManager with specific configuration components.

        :param metadata: Project metadata.
        :param cmake_settings: CMake settings.
        :param dependencies: Project dependencies.
        :param structure: Project directory structure.
        :param project_path: Path to the project directory.
        """
        self.metadata = metadata
        self.cmake_settings = cmake_settings
        self.dependencies = dependencies
        self.structure = structure
        self.project_path = Path(project_path).absolute()
        self.logger = logging.getLogger(__name__)

    def configure_cmake(self) -> None:
        """
        Configure CMake by generating a CMakeLists.txt file in the CMake directory.
        """
        try:
            # Define the path for the CMakeLists.txt file
            cmake_dir = self.project_path / "cmake"
            cmake_file_path = cmake_dir / "CMakeLists.txt"

            # Use CMakeBuilder to generate the CMake content
            builder = CMakeBuilder()
            builder.set_metadata(self.metadata)
            builder.set_cmake_settings(self.cmake_settings)
            builder.set_dependencies(self.dependencies)
            builder.set_structure(self.structure)
            builder.set_output_path(cmake_file_path)
            builder.build()

            self.logger.info(f"CMake configuration written to {cmake_file_path}")
        except Exception as e:
            self.logger.error(f"Failed to configure CMake: {e}")
            raise
