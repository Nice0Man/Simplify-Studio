from modules.simplify_studio.core.cmake_manager.manager import CMakeManager
from modules.simplify_studio.core.compiler_manager.manager import CompilerConfigManager
from modules.simplify_studio.core.config.loader import ProjectConfig
from modules.simplify_studio.core.dep_manager.manager import DependencyManager
from modules.simplify_studio.core.directory_manager.manager import DirectoryManager


class Project:
    """
    Represents a CMake C/C++ project, configured using various managers.
    """

    def __init__(self, config_file: str, project_path: str):
        """
        Initialize the Project.

        Args:
            config_file: Path to the project configuration file.
            project_path: Path to the project directory.
        """
        self.config = ProjectConfig(config_file)
        self.project_path = project_path
        self.metadata = self.config.get_project_metadata()
        self.structure = self.config.get_structure()
        self.dependencies = self.config.get_dependencies()
        self.compiler_settings = self.config.get_compiler_settings()
        self.cmake_settings = self.config.get_cmake_settings()

        self.directory_manager = DirectoryManager(self.project_path, self.structure)
        self.dependency_manager = DependencyManager(self.project_path, self.dependencies)
        self.compiler_manager = CompilerConfigManager(self.compiler_settings)
        self.cmake_manager = CMakeManager(
            self.metadata, self.cmake_settings, self.dependencies, self.structure, project_path
        )

    def setup(self) -> None:
        """
        Set up the project by configuring directories, dependencies, compiler, and CMake.
        """
        self.directory_manager.create_directories()
        self.dependency_manager.install_dependencies()
        self.compiler_manager.configure_compiler()
        self.cmake_manager.configure_cmake()
