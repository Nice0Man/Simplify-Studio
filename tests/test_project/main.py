import logging

from modules.simplify_studio.core.project.project import Project


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    project_path = "./my_cmake_project"  # Define the project path
    project = Project("project_structure.yaml", project_path)

    # Set up the project
    project.setup()
    logger.info("Project setup complete.")


if __name__ == "__main__":
    main()
