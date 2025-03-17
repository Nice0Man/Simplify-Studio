import pytest

from modules.simplify_studio.core.cmake_manager.factory import CMakeCommandFactory
from modules.simplify_studio.core.cmake_manager.template import (
    CMakeTemplate,
    CMakeProjectTemplate,
    CMakeIncludeTemplate,
    CMakeAddExecutableTemplate,
)


class TestCMakeCommandFactory:

    # Successfully registers all CMakeTemplate subclasses from the template module
    def test_register_commands_registers_all_template_subclasses(self, mocker):
        # Arrange
        mock_template_classes = {
            "CMakeProjectTemplate": type(
                "CMakeProjectTemplate", (CMakeTemplate,), {"command_key": "project"}
            ),
            "CMakeAddLibraryTemplate": type(
                "CMakeAddLibraryTemplate", (CMakeTemplate,), {"command_key": "add_library"}
            ),
            "NonTemplateClass": type("NonTemplateClass", (), {}),
            "AbstractTemplate": type(
                "AbstractTemplate", (CMakeTemplate,), {"__abstractmethods__": {"generate"}}
            ),
        }

        mocker.patch(
            "modules.simplify_studio.core.cmake_manager.factory.dir",
            return_value=mock_template_classes.keys(),
        )
        mocker.patch(
            "modules.simplify_studio.core.cmake_manager.factory.isabstract",
            side_effect=lambda cls: cls.__name__ == "AbstractTemplate",
        )
        mocker.patch(
            "modules.simplify_studio.core.cmake_manager.factory.getattr",
            side_effect=lambda mod, name: mock_template_classes.get(name),
        )

        # Reset registry for clean test
        CMakeCommandFactory._command_registry = {}

        # Act
        CMakeCommandFactory.register_commands()

        # Assert
        assert len(CMakeCommandFactory._command_registry) == 2
        assert "project" in CMakeCommandFactory._command_registry
        assert "add_library" in CMakeCommandFactory._command_registry

    # Creates a command instance using a valid command key
    def test_create_command_with_valid_key(self, mocker):
        # Arrange
        mock_template = mocker.Mock(spec=CMakeTemplate)
        mock_template.generate.return_value = "project(MyProject LANGUAGES C CXX)"
        mock_template_class = mocker.Mock(return_value=mock_template)

        # Setup registry with mock template
        CMakeCommandFactory._command_registry = {"project": mock_template_class}

        # Act
        result = CMakeCommandFactory.create_command(
            "project", project_name="MyProject", languages=["C", "CXX"]
        )

        # Assert
        assert result == "project(MyProject LANGUAGES C CXX)"
        mock_template_class.assert_called_once()
        mock_template.generate.assert_called_once_with(
            project_name="MyProject", languages=["C", "CXX"]
        )

    # Handles multiple command registrations correctly
    def test_register_commands_handles_multiple_registrations(self, mocker):
        # Arrange
        # Create a set of template classes with different command keys
        template_classes = {
            "CMakeProjectTemplate": type(
                "CMakeProjectTemplate", (CMakeTemplate,), {"command_key": "project"}
            ),
            "CMakeAddLibraryTemplate": type(
                "CMakeAddLibraryTemplate", (CMakeTemplate,), {"command_key": "add_library"}
            ),
            "CMakeSetTemplate": type("CMakeSetTemplate", (CMakeTemplate,), {"command_key": "set"}),
        }

        # Mock the template module inspection
        mocker.patch(
            "modules.simplify_studio.core.cmake_manager.factory.dir",
            return_value=template_classes.keys(),
        )
        mocker.patch(
            "modules.simplify_studio.core.cmake_manager.factory.isabstract", return_value=False
        )
        mocker.patch(
            "modules.simplify_studio.core.cmake_manager.factory.getattr",
            side_effect=lambda mod, name: template_classes.get(name),
        )

        # Reset registry
        CMakeCommandFactory._command_registry = {}

        # Act
        CMakeCommandFactory.register_commands()

        # Assert
        assert len(CMakeCommandFactory._command_registry) == 3
        assert "project" in CMakeCommandFactory._command_registry
        assert "add_library" in CMakeCommandFactory._command_registry
        assert "set" in CMakeCommandFactory._command_registry

    # Command keys are properly extracted from template instances
    def test_command_keys_properly_extracted(self, mocker):
        # Arrange
        # Create a custom template class with a specific command key
        class CustomTemplate(CMakeTemplate):
            def __init__(self):
                super().__init__()
                self.command_key = "custom_command"

            def generate(self, **kwargs):
                return f"{self.command_key}()"

        # Mock the template module to return our custom class
        mocker.patch(
            "modules.simplify_studio.core.cmake_manager.factory.dir",
            return_value=["CustomTemplate"],
        )
        mocker.patch(
            "modules.simplify_studio.core.cmake_manager.factory.isabstract", return_value=False
        )
        mocker.patch(
            "modules.simplify_studio.core.cmake_manager.factory.getattr",
            return_value=CustomTemplate,
        )
        mocker.patch(
            "modules.simplify_studio.core.cmake_manager.factory.issubclass", return_value=True
        )

        # Reset registry
        CMakeCommandFactory._command_registry = {}

        # Act
        CMakeCommandFactory.register_commands()

        # Assert
        assert "custom_command" in CMakeCommandFactory._command_registry
        assert CMakeCommandFactory._command_registry["custom_command"] == CustomTemplate

    # Handles case when no template classes are found in the module
    def test_register_commands_with_no_template_classes(self, mocker):
        # Arrange
        # Mock empty dir result
        mocker.patch("modules.simplify_studio.core.cmake_manager.factory.dir", return_value=[])

        # Reset registry
        CMakeCommandFactory._command_registry = {}

        # Act
        CMakeCommandFactory.register_commands()

        # Assert
        assert len(CMakeCommandFactory._command_registry) == 0

    # Raises ValueError when an unknown command key is provided
    def test_create_command_with_unknown_key_raises_error(self):
        # Arrange
        # Setup registry with a known command
        CMakeCommandFactory._command_registry = {"project": CMakeProjectTemplate}

        # Act & Assert
        with pytest.raises(ValueError) as excinfo:
            CMakeCommandFactory.create_command("unknown_command")

        # Verify error message contains available commands
        assert "Unknown command key: unknown_command" in str(excinfo.value)
        assert "Available commands: project" in str(excinfo.value)

    # Handles command keys that are empty strings
    def test_create_command_with_empty_key(self):
        # Arrange
        # Create a template with empty command key
        class EmptyKeyTemplate(CMakeTemplate):
            def __init__(self):
                super().__init__()
                self.command_key = ""

            def generate(self, **kwargs):
                return "empty_command()"

        # Setup registry with the empty key template
        CMakeCommandFactory._command_registry = {"": EmptyKeyTemplate}

        # Act
        result = CMakeCommandFactory.create_command("")

        # Assert
        assert result == "empty_command()"

    # Properly handles case when template module has no CMakeTemplate subclasses
    def test_register_commands_with_no_cmake_template_subclasses(self, mocker):
        # Arrange
        # Create non-template classes
        non_template_classes = {
            "NonTemplateClass1": type("NonTemplateClass1", (), {}),
            "NonTemplateClass2": type("NonTemplateClass2", (), {}),
        }

        # Mock the template module inspection to return non-template classes
        mocker.patch(
            "modules.simplify_studio.core.cmake_manager.factory.dir",
            return_value=non_template_classes.keys(),
        )
        mocker.patch(
            "modules.simplify_studio.core.cmake_manager.factory.getattr",
            side_effect=lambda mod, name: non_template_classes.get(name),
        )
        mocker.patch(
            "modules.simplify_studio.core.cmake_manager.factory.issubclass", return_value=False
        )

        # Reset registry
        CMakeCommandFactory._command_registry = {}

        # Act
        CMakeCommandFactory.register_commands()

        # Assert
        assert len(CMakeCommandFactory._command_registry) == 0

    # Handles kwargs that don't match the expected parameters for a template's generate method
    def test_create_command_with_invalid_kwargs(self, mocker):
        # Arrange
        # Create a template with specific parameter requirements
        class StrictTemplate(CMakeTemplate):
            def __init__(self):
                super().__init__()
                self.command_key = "strict"

            def generate(self, required_param):
                return f"strict({required_param})"

        # Mock the template class
        mock_template = StrictTemplate()
        mocker.spy(mock_template, "generate")
        mock_template_class = mocker.Mock(return_value=mock_template)

        # Setup registry
        CMakeCommandFactory._command_registry = {"strict": mock_template_class}

        # Act & Assert
        with pytest.raises(TypeError) as excinfo:
            CMakeCommandFactory.create_command("strict", wrong_param="value")

        # Verify error is about missing required parameter
        assert "required_param" in str(excinfo.value)

    # Provides helpful error message listing available commands when key not found
    def test_error_message_for_unknown_command_key(self):
        CMakeCommandFactory.register_commands()
        unknown_key = "non_existent_command"
        expected_message = "Unknown command key: non_existent_command. Available commands: "
        with pytest.raises(ValueError) as excinfo:
            CMakeCommandFactory.create_command(unknown_key)
        assert expected_message in str(excinfo.value)

    # Registry is properly maintained as a class variable
    def test_registry_maintained_as_class_variable(self):
        CMakeCommandFactory.register_commands()
        assert isinstance(CMakeCommandFactory._command_registry, dict)
        assert len(CMakeCommandFactory._command_registry) > 0

    # Command registration is idempotent (calling register_commands multiple times)
    def test_idempotent_command_registration(self):
        CMakeCommandFactory.register_commands()
        initial_registry_size = len(CMakeCommandFactory._command_registry)
        CMakeCommandFactory.register_commands()
        assert len(CMakeCommandFactory._command_registry) == initial_registry_size

    # Properly filters abstract classes during registration
    def test_register_commands_filters_abstract_classes(self, mocker):
        # Mock the template module to include an abstract class
        mock_template = mocker.patch("modules.simplify_studio.core.cmake_manager.factory.template")
        mock_abstract_class = mocker.Mock(spec=CMakeTemplate, command_key=None)
        mocker.patch("inspect.isabstract", return_value=True)
        mock_template.AbstractClass = mock_abstract_class

        # Register commands
        CMakeCommandFactory.register_commands()

        # Assert that the abstract class is not registered
        assert "AbstractClass" not in CMakeCommandFactory._command_registry

    # Instantiates the correct template class based on the provided command key
    def test_create_command_instantiates_correct_class(self, mocker):
        # Mock the template module and a concrete class
        mock_template = mocker.patch("modules.simplify_studio.core.cmake_manager.factory.template")
        mock_concrete_class = mocker.Mock(spec=CMakeTemplate, command_key="mock_command")
        mock_concrete_class().generate.return_value = "mock_command_output"
        mock_template.ConcreteClass = mock_concrete_class

        # Register commands
        CMakeCommandFactory.register_commands()

        # Create command and assert the correct class is instantiated
        result = CMakeCommandFactory.create_command("mock_command")
        assert result == "mock_command_output"
        mock_concrete_class().generate.assert_called_once_with()

    # Handles template classes that don't have command_key attribute
    def test_register_commands_handles_missing_command_key(self, mocker):
        # Mock the template module to include a class without command_key
        mock_template = mocker.patch("modules.simplify_studio.core.cmake_manager.factory.template")
        mock_class_without_key = mocker.Mock(spec=CMakeTemplate)
        delattr(mock_class_without_key, "command_key")
        mock_template.ClassWithoutKey = mock_class_without_key

        # Register commands
        CMakeCommandFactory.register_commands()

        # Assert that the class without command_key is not registered
        assert "ClassWithoutKey" not in CMakeCommandFactory._command_registry

    # Registers concrete CMakeTemplate subclasses but ignores abstract ones
    def test_register_concrete_templates_only(self, mocker):
        # Mock the template module to include both abstract and concrete classes
        mock_template = mocker.patch("modules.simplify_studio.core.cmake_manager.factory.template")
        mock_template.AbstractTemplate = type(
            "AbstractTemplate", (CMakeTemplate,), {"__abstractmethods__": frozenset(["generate"])}
        )
        mock_template.ConcreteTemplate = type(
            "ConcreteTemplate",
            (CMakeTemplate,),
            {"command_key": "concrete", "generate": lambda self, **kwargs: "command"},
        )

        # Register commands
        CMakeCommandFactory.register_commands()

        # Assert only the concrete template is registered
        assert "concrete" in CMakeCommandFactory._command_registry
        assert CMakeCommandFactory._command_registry["concrete"] == mock_template.ConcreteTemplate
        assert "AbstractTemplate" not in CMakeCommandFactory._command_registry

    # Error message includes the specific unknown command key
    def test_error_message_includes_unknown_key(self):
        # Ensure the registry is empty
        CMakeCommandFactory._command_registry.clear()

        # Attempt to create a command with an unknown key
        unknown_key = "unknown"
        with pytest.raises(ValueError) as excinfo:
            CMakeCommandFactory.create_command(unknown_key)

        # Check that the error message includes the unknown key
        assert f"Unknown command key: {unknown_key}" in str(excinfo.value)

    # Correctly maps each template's command_key to its class in the registry
    def test_register_commands_maps_command_keys(self, mocker):
        # Mock the template module to simulate the presence of CMakeTemplate subclasses
        mock_template = mocker.patch("modules.simplify_studio.core.cmake_manager.factory.template")
        mock_template.CMakeProjectTemplate = CMakeProjectTemplate
        mock_template.CMakeIncludeTemplate = CMakeIncludeTemplate

        # Register commands
        CMakeCommandFactory.register_commands()

        # Assert that the command keys are correctly mapped to their classes
        assert CMakeCommandFactory._command_registry["project"] == CMakeProjectTemplate
        assert CMakeCommandFactory._command_registry["include"] == CMakeIncludeTemplate

    # Handles registration of multiple CMakeTemplate subclasses in a single call
    def test_register_multiple_templates_in_single_call(self, mocker):
        # Mock the template module to simulate multiple CMakeTemplate subclasses
        mock_template = mocker.patch("modules.simplify_studio.core.cmake_manager.factory.template")
        mock_template.CMakeProjectTemplate = CMakeProjectTemplate
        mock_template.CMakeAddExecutableTemplate = CMakeAddExecutableTemplate

        # Register commands
        CMakeCommandFactory.register_commands()

        # Assert that multiple templates are registered in a single call
        assert "project" in CMakeCommandFactory._command_registry
        assert "add_executable" in CMakeCommandFactory._command_registry

    # Only registers classes that have the command_key attribute
    def test_register_only_classes_with_command_key(self, mocker):
        # Mock the template module to simulate classes with and without command_key
        class NoCommandKeyTemplate(CMakeTemplate):
            def generate(self, **kwargs) -> str:
                return "no_command_key"

        mock_template = mocker.patch("modules.simplify_studio.core.cmake_manager.factory.template")
        mock_template.CMakeProjectTemplate = CMakeProjectTemplate
        mock_template.NoCommandKeyTemplate = NoCommandKeyTemplate

        # Register commands
        CMakeCommandFactory.register_commands()

        # Assert that only classes with command_key are registered
        assert "project" in CMakeCommandFactory._command_registry
        assert "no_command_key" not in CMakeCommandFactory._command_registry
