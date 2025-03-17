from modules.simplify_studio.core.config.loader import Metadata, CMakeSettings


class CMakeCommandStrategy:
    """
    Base class for CMake command strategies.
    """

    def generate(self) -> str:
        """
        Generate the CMake command string.

        :return: str - The CMake command string.
        """
        raise NotImplementedError("Subclasses should implement this method.")


class CMakeHeaderStrategy(CMakeCommandStrategy):
    def __init__(self, metadata: Metadata, cmake_settings: CMakeSettings):
        self.metadata = metadata
        self.cmake_settings = cmake_settings

    def generate(self) -> str:
        """
        Generate the CMake header command string.

        :return: str - The CMake header command string.
        """
        return CMAKE_HEADER_TEMPLATE.format(
            cmake_version=self.cmake_settings.options.get("CMAKE_MINIMUM_REQUIRED_VERSION", "3.10"),
            project_name=self.metadata.name,
            project_version=self.metadata.version,
        )


class CMakeCompilerSettingsStrategy(CMakeCommandStrategy):
    def __init__(self, cmake_settings: CMakeSettings):
        self.cmake_settings = cmake_settings

    def generate(self) -> str:
        """
        Generate the CMake compiler settings command string.

        :return: str - The CMake compiler settings command string.
        """
        flags = " ".join(self.cmake_settings.options.get("flags", []))
        return CMAKE_COMPILER_SETTINGS_TEMPLATE.format(
            cxx_standard=self.cmake_settings.options.get("CMAKE_CXX_STANDARD", 17), flags=flags
        )


class CMakeIncludeDirectoriesStrategy(CMakeCommandStrategy):
    def __init__(self, structure: Dict[str, DirectoryNode]):
        self.structure = structure

    def generate(self) -> str:
        """
        Generate the CMake include directories command string.

        :return: str - The CMake include directories command string.
        """
        include_dirs = []
        for dir_name, directory_node in self.structure.items():
            if dir_name == "src":
                include_dirs.append(CMAKE_INCLUDE_DIRECTORIES_TEMPLATE.format(directory=dir_name))
                for subdir in directory_node:
                    include_dirs.append(
                        CMAKE_INCLUDE_DIRECTORIES_TEMPLATE.format(
                            directory=f"{dir_name}/{subdir.name}"
                        )
                    )
        return "\n".join(include_dirs)


class CMakeSourceFilesStrategy(CMakeCommandStrategy):
    def __init__(self, structure: Dict[str, DirectoryNode]):
        self.structure = structure

    def generate(self) -> str:
        """
        Generate the CMake source files command string.

        :return: str - The CMake source files command string.
        """
        source_files = []
        for dir_name, directory_node in self.structure.items():
            if dir_name == "src":
                for subdir in directory_node:
                    source_files.append(
                        CMAKE_SOURCE_FILES_TEMPLATE.format(
                            subdir_name=subdir.name, directory=dir_name
                        )
                    )
        return "\n".join(source_files)


class CMakeDependenciesStrategy(CMakeCommandStrategy):
    def __init__(self, dependencies: Dict[str, Dependency]):
        self.dependencies = dependencies

    def generate(self) -> str:
        """
        Generate the CMake dependencies command string.

        :return: str - The CMake dependencies command string.
        """
        dependency_commands = []
        for name, dependency in self.dependencies.items():
            dependency_commands.append(
                CMAKE_DEPENDENCIES_TEMPLATE.format(name=name, git_repo=dependency.git)
            )
        return "\n".join(dependency_commands)


class CMakeCustomCommandsStrategy(CMakeCommandStrategy):
    def __init__(self, cmake_settings: CMakeSettings):
        self.custom_commands = cmake_settings.options.get("custom_commands", [])

    def generate(self) -> str:
        """
        Generate the CMake custom commands string.

        :return: str - The CMake custom commands string.
        """
        return "\n".join(self.custom_commands)
