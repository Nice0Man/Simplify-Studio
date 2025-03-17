import os
from dataclasses import dataclass, field
from typing import Dict, Any, List

import yaml

from modules.simplify_studio.core.directory_manager.manager import DirectoryNode


@dataclass
class Metadata:
    name: str
    version: str
    author: str

@dataclass
class Dependency:
    git: str
    version: str = ""
    branch: str = ""
    tag: str = ""
    commit: str = ""
    dependency_folder: str = ""
    additional_fields: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        for key, value in self.additional_fields.items():
            setattr(self, key, value)


@dataclass
class CompilerSettings:
    compiler_type: str
    compiler_path: str
    cxx_standard: int
    flags: List[str]
    defines: List[str]


@dataclass
class CMakeSettings:
    build_type: str
    options: Dict[str, Any]


class ProjectConfig:
    """
    Loads and manages project configuration from a YAML file.
    """

    def __init__(self, config_file: str):
        """
        Initialize the ProjectConfig.

        Args:
            config_file: Path to the YAML configuration file.
        """
        self.config = self._load_config(config_file)

    @staticmethod
    def _load_config(config_file: str) -> dict:
        """
        Load the configuration from a YAML file.

        Args:
            config_file: Path to the YAML file.

        Returns:
            dict: Configuration dictionary.

        Raises:
            FileNotFoundError: If the configuration file doesn't exist.
            ConfigError: If there's an error parsing the configuration.
        """
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file not found: {config_file}")

        try:
            with open(config_file, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)

            if not isinstance(config, dict):
                raise ValueError(f"Invalid configuration format in {config_file}")

            return config
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML configuration: {e}")

    def get_project_metadata(self) -> Metadata:
        """
        Get the project metadata from the configuration.

        Returns:
            Metadata: Project metadata including name, version, and author.
        """
        return Metadata(
            name=self.config.get("project_name", ""),
            version=self.config.get("version", ""),
            author=self.config.get("author", ""),
        )

    def get_structure(self) -> Dict[str, DirectoryNode]:
        """
        Get the project directory structure from the configuration.

        Returns:
            dict: Project directory structure as a tree of DirectoryNode objects.
        """
        directories = self.config.get("directories", {})
        parsed_structure = {}

        def parse_directory(name: str, details: Any) -> DirectoryNode:
            """
            Parse a directory and its details into a DirectoryNode object.

            Args:
                name: The name of the directory.
                details: A dictionary or list containing directory details.

            Returns:
                DirectoryNode: A DirectoryNode object representing the directory.
            """
            node = DirectoryNode(name=name)
            if isinstance(details, list):
                for detail in details:
                    if isinstance(detail, dict):
                        for sub_name, sub_details in detail.items():
                            node.add_subdirectory(parse_directory(sub_name, sub_details))
                    elif isinstance(detail, str):
                        node.description = detail
            elif isinstance(details, dict):
                for sub_name, sub_details in details.items():
                    node.add_subdirectory(parse_directory(sub_name, sub_details))
            return node

        for dir_name, dir_details in directories.items():
            parsed_structure[dir_name] = parse_directory(dir_name, dir_details)

        return parsed_structure

    def get_dependencies(self) -> Dict[str, Dependency]:
        """
        Get the project dependencies from the configuration.

        Returns:
            dict: Project dependencies with optional branch, tag, and commit.
        """
        dependencies = self.config.get("dependencies", {})
        return {
            name: Dependency(
                git=details.get("git", ""),
                version=details.get("version", ""),
                branch=details.get("branch", ""),
                tag=details.get("tag", ""),
                commit=details.get("commit", ""),
                dependency_folder=details.get("dependency_folder", name),
                additional_fields={
                    k: v
                    for k, v in details.items()
                    if k not in {"git", "version", "branch", "tag", "commit", "dependency_folder"}
                },
            )
            for name, details in dependencies.items()
        }

    def get_compiler_settings(self) -> CompilerSettings:
        """
        Get the compiler settings from the configuration.

        Returns:
            CompilerSettings: Compiler settings including compiler type, path, C++ standard, flags, and defines.
        """
        compiler_config = self.config.get("compiler", {})
        return CompilerSettings(
            compiler_type=compiler_config.get("compiler_type", "gcc"),
            compiler_path=compiler_config.get("compiler_path", ""),
            cxx_standard=compiler_config.get("cxx_standard", 11),
            flags=compiler_config.get("flags", []),
            defines=compiler_config.get("defines", []),
        )

    def get_cmake_settings(self) -> CMakeSettings:
        """
        Get the CMake settings from the configuration.

        Returns:
            CMakeSettings: CMake settings including build type and options.
        """
        cmake_config = self.config.get("cmake", {})
        return CMakeSettings(
            build_type=cmake_config.get("build_type", "Release"),
            options=cmake_config.get("options", {}),
        )
