import os
from pathlib import Path
from typing import Dict, List

from modules.simplify_studio.core.cmake_manager.command import (
    CMakeHeaderCommand,
    CMakeCompilerSettingsCommand,
    CMakeIncludeDirectoriesCommand,
    CMakeSourceFilesCommand,
    CMakeDependenciesCommand,
    CMakeCommand,
    CMakeCustomCommandsCommand,
)
from modules.simplify_studio.core.config.loader import (
    Metadata,
    CMakeSettings,
    Dependency,
    DirectoryNode,
)


# class CMakeCommandFactory:
#     def __init__(
#         self,
#         metadata: Metadata,
#         cmake_settings: CMakeSettings,
#         dependencies: Dict[str, Dependency],
#         structure: Dict[str, DirectoryNode],
#     ):
#         self.metadata = metadata
#         self.cmake_settings = cmake_settings
#         self.dependencies = dependencies
#         self.structure = structure
#
#     def create_commands(self) -> List[CMakeCommand]:
#         """
#         Create a list of CMake command objects.
#
#         :return: List[CMakeCommand] - A list of CMake command objects.
#         """
#         commands = [
#             CMakeHeaderCommand(self.metadata, self.cmake_settings),
#             CMakeCompilerSettingsCommand(self.cmake_settings),
#             CMakeIncludeDirectoriesCommand(self.structure),
#             CMakeSourceFilesCommand(self.structure),
#             CMakeDependenciesCommand(self.dependencies),
#             CMakeCustomCommandsCommand(self.cmake_settings, self.dependencies),
#         ]
#         return commands


class CMakeBuilder:
    """
    Builder class for generating a CMakeLists.txt file.
    """

    def __init__(self):
        self.metadata: Metadata | None = None
        self.cmake_settings: CMakeSettings | None = None
        self.dependencies: Dict[str, Dependency] | None = None
        self.structure: Dict[str, DirectoryNode] | None = None
        self.output_path: Path | None = None

    def set_metadata(self, metadata: Metadata):
        self.metadata = metadata

    def set_cmake_settings(self, cmake_settings: CMakeSettings):
        self.cmake_settings = cmake_settings

    def set_dependencies(self, dependencies: Dict[str, Dependency]):
        self.dependencies = dependencies

    def set_structure(self, structure: Dict[str, DirectoryNode]):
        self.structure = structure

    def set_output_path(self, output_path: Path):
        self.output_path = output_path

    def build(self) -> None:
        """
        Generate the CMakeLists.txt file based on the provided configuration.
        """

        factory = CMakeCommandFactory(
            self.metadata, self.cmake_settings, self.dependencies, self.structure
        )
        commands = factory.create_commands()
        cmake_content = "\n\n".join(str(command) for command in commands)
        self._write_to_file(cmake_content)

    def _write_to_file(self, content: str) -> None:
        """
        Write the generated content to the CMakeLists.txt file.

        :param content: The content to write to the file.
        """
        os.makedirs(self.output_path.parent, exist_ok=True)
        with open(self.output_path, "w") as cmake_file:
            cmake_file.write(content)
