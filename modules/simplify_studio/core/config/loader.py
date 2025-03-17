class ProjectConfig:
    def __init__(
        self, enable_testing: bool, generate_build_system: bool, cmake_options: dict
    ):
        self.enable_testing = enable_testing
        self.generate_build_system = generate_build_system
        self.cmake_options = cmake_options
