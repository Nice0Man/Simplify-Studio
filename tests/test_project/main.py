#!/usr/bin/env python3
"""
Entry point for using the ProjectBuilder to create and manage a CMake C/C++ project.
"""

import logging

from modules.simplify_studio.core.config.loader import ProjectConfig
from modules.simplify_studio.core.project_builder.builder import ProjectBuilder


def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Define project details
    project_name = "MyCMakeProject"
    project_path = r"C:\Users\ekrot\VSCodeProjects\Simplify-Studio\tests\test_project"

    # Create a project configuration
    config = ProjectConfig(
        enable_testing=True,
        generate_build_system=True,
        cmake_options={
            "CMAKE_CXX_STANDARD": "17",
            "CMAKE_EXPORT_COMPILE_COMMANDS": "ON",
        },
    )

    # Initialize the ProjectBuilder
    builder = ProjectBuilder(project_name, project_path, config)

    # Create the project
    if builder.create_project():
        logging.info("Project created successfully.")

        # Add a library
        if builder.add_library("MyLibrary"):
            logging.info("Library 'MyLibrary' added successfully.")

        # Add an executable
        if builder.add_executable("MyExecutable"):
            logging.info("Executable 'MyExecutable' added successfully.")

        # Generate the build system
        if builder.generate_build_system():
            logging.info("Build system generated successfully.")

        # Build the project
        if builder.build():
            logging.info("Project built successfully.")

        # Run tests
        if builder.run_tests():
            logging.info("All tests passed successfully.")
    else:
        logging.error("Failed to create the project.")


if __name__ == "__main__":
    main()
