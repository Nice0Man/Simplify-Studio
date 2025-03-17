import pytest

from modules.simplify_studio.core.cmake_manager.template import (
    CMakeProjectTemplate,
    CMakeTemplate,
    CMakeSetPropertyTemplate,
    CMakeFileOperationsTemplate,
    CMakeAddExecutableTemplate,
    CMakeIfTemplate,
    CMakeAddLibraryTemplate,
    CMakeFindLibraryTemplate,
    CMakeForeachTemplate,
    CMakeMessageTemplate,
    CMakeIncludeTemplate,
    CMakeTargetIncludeDirectoriesTemplate,
    CMakeSetTemplate,
)


class TestCodeUnderTest:
    # Each template class correctly generates CMake command strings with proper syntax
    def test_cmake_project_template_generates_correct_syntax(self):
        # Arrange
        template = CMakeProjectTemplate()
        project_name = "MyProject"
        languages = ["CXX", "C"]

        # Act
        result = template.generate(project_name=project_name, languages=languages)

        # Assert
        assert result == "project(MyProject LANGUAGES CXX C)"

    # Abstract base class enforces implementation of generate method in subclasses
    def test_abstract_base_class_cannot_be_instantiated(self):
        # Act & Assert
        with pytest.raises(TypeError):
            CMakeTemplate()  # Should raise TypeError as it's an abstract class

    # Template classes handle basic input parameters correctly
    def test_cmake_set_template_handles_parameters_correctly(self):
        # Arrange
        template = CMakeSetTemplate()
        variable = "CMAKE_CXX_STANDARD"
        value = "17"

        # Act
        result = template.generate(variable=variable, value=value)

        # Assert
        assert result == "set(CMAKE_CXX_STANDARD 17)"

    # Template classes with list parameters join elements with spaces
    def test_cmake_add_executable_joins_source_list_with_spaces(self):
        # Arrange
        template = CMakeAddExecutableTemplate()
        target_name = "my_app"
        sources = ["main.cpp", "utils.cpp", "app.cpp"]

        # Act
        result = template.generate(target_name=target_name, sources=sources)

        # Assert
        assert result == "add_executable(my_app main.cpp utils.cpp app.cpp)"

    # Template classes with dictionary parameters format key-value pairs correctly
    def test_cmake_set_property_formats_dictionary_correctly(self):
        # Arrange
        template = CMakeSetPropertyTemplate()
        target = "my_lib"
        properties = {"CXX_STANDARD": "17", "POSITION_INDEPENDENT_CODE": "ON"}

        # Act
        result = template.generate(target=target, properties=properties)

        # Assert
        # Note: Dictionary order is not guaranteed, so we check for both possible orderings
        possible_results = [
            "set_target_properties(my_lib PROPERTIES CXX_STANDARD 17 POSITION_INDEPENDENT_CODE ON)",
            "set_target_properties(my_lib PROPERTIES POSITION_INDEPENDENT_CODE ON CXX_STANDARD 17)",
        ]
        assert result in possible_results

    # Empty lists passed to templates that expect list parameters
    def test_cmake_target_include_directories_with_empty_list(self):
        # Arrange
        template = CMakeTargetIncludeDirectoriesTemplate()
        target_name = "my_target"
        directories = []

        # Act
        result = template.generate(target_name=target_name, directories=directories)

        # Assert
        assert result == "target_include_directories(my_target PRIVATE )"

    # None values passed to optional parameters
    def test_cmake_find_library_with_none_paths(self):
        # Arrange
        template = CMakeFindLibraryTemplate()
        library_name = "MyLib"

        # Act
        result = template.generate(library_name=library_name, paths=None)

        # Assert
        assert result == "find_library(MyLib )"

    # Empty strings passed as required parameters
    def test_cmake_include_with_empty_string(self):
        # Arrange
        template = CMakeIncludeTemplate()
        file = ""

        # Act
        result = template.generate(file=file)

        # Assert
        assert result == "include()"

    # Very long strings or lists that might affect command readability
    def test_cmake_add_library_with_many_source_files(self):
        # Arrange
        template = CMakeAddLibraryTemplate()
        lib_name = "huge_lib"
        sources = [f"src{i}.cpp" for i in range(50)]  # Generate 50 source files

        # Act
        result = template.generate(lib_name=lib_name, sources=sources)

        # Assert
        expected = (
            "add_library(huge_lib STATIC " + " ".join([f"src{i}.cpp" for i in range(50)]) + ")"
        )
        assert result == expected
        assert len(result.split()) == 52  # 'add_library(huge_lib' + lib_type + 50 source files

    # Special characters in strings that might need escaping
    def test_cmake_message_with_special_characters(self):
        # Arrange
        template = CMakeMessageTemplate()
        message_type = "STATUS"
        message = 'Special chars: " \\ $ ; # *'

        # Act
        result = template.generate(message_type=message_type, message=message)

        # Assert
        assert result == 'message(STATUS "Special chars: " \\ $ ; # *")'

    # Conditional templates (CMakeIfTemplate) properly format multi-line commands
    def test_cmake_if_template_multiline_formatting(self):
        template = CMakeIfTemplate()
        condition = "DEFINED MY_VAR"
        commands = ['message(STATUS "Variable is defined")', "set(MY_VAR 1)"]
        expected_output = (
            'if(DEFINED MY_VAR)\n  message(STATUS "Variable is defined")\n  set(MY_VAR 1)\nendif()'
        )
        assert template.generate(condition, commands) == expected_output

        # Generate a simple if block with a single command

    def test_simple_if_block_with_single_command(self):
        # Arrange
        template = CMakeIfTemplate()
        condition = "EXISTS file.txt"
        commands = ['message(STATUS "File exists")']

        # Act
        result = template.generate(condition=condition, commands=commands)

        # Assert
        expected = 'if(EXISTS file.txt)\n  message(STATUS "File exists")\nendif()'
        assert result == expected

    # Generate an if block with multiple commands
    def test_if_block_with_multiple_commands(self):
        # Arrange
        template = CMakeIfTemplate()
        condition = "DEFINED VAR"
        commands = [
            'message(STATUS "VAR is defined")',
            "set(RESULT TRUE)",
            "add_subdirectory(src)",
        ]

        # Act
        result = template.generate(condition=condition, commands=commands)

        # Assert
        expected = 'if(DEFINED VAR)\n  message(STATUS "VAR is defined")\n  set(RESULT TRUE)\n  add_subdirectory(src)\nendif()'
        assert result == expected

    # Verify proper indentation of commands within the if block
    def test_proper_indentation_of_commands(self):
        # Arrange
        template = CMakeIfTemplate()
        condition = "APPLE"
        commands = ["set(OS_APPLE TRUE)", "include(AppleConfig)"]

        # Act
        result = template.generate(condition=condition, commands=commands)

        # Assert
        assert "if(APPLE)\n  set(OS_APPLE TRUE)\n  include(AppleConfig)\nendif()" == result
        # Verify each command is indented with two spaces
        lines = result.split("\n")
        for i in range(1, len(lines) - 1):
            assert lines[i].startswith("  ")

    # Check that the condition is properly enclosed in parentheses
    def test_condition_enclosed_in_parentheses(self):
        # Arrange
        template = CMakeIfTemplate()
        condition = "WIN32 AND MSVC"
        commands = ["set(USING_MSVC TRUE)"]

        # Act
        result = template.generate(condition=condition, commands=commands)

        # Assert
        assert result.startswith(f"if({condition})")
        assert ")" in result.split("\n")[0]

    # Verify the command_key is set to "if" in the constructor
    def test_command_key_set_to_if(self):
        # Arrange & Act
        template = CMakeIfTemplate()

        # Assert
        assert template.command_key == "if"

        # Verify the command key is used in the generated output
        result = template.generate(condition="TRUE", commands=['message(STATUS "True condition")'])
        assert result.startswith("if(")

    # Handle empty condition string
    def test_empty_condition_string(self):
        # Arrange
        template = CMakeIfTemplate()
        condition = ""
        commands = ['message(STATUS "Empty condition")']

        # Act
        result = template.generate(condition=condition, commands=commands)

        # Assert
        expected = 'if()\n  message(STATUS "Empty condition")\nendif()'
        assert result == expected

    # Handle empty commands list
    def test_empty_commands_list(self):
        # Arrange
        template = CMakeIfTemplate()
        condition = "UNIX"
        commands = []

        # Act
        result = template.generate(condition=condition, commands=commands)

        # Assert
        expected = "if(UNIX)\n  \nendif()"
        assert result == expected

    # Handle commands with special characters or quotes
    def test_commands_with_special_characters(self):
        # Arrange
        template = CMakeIfTemplate()
        condition = "DEFINED MY_VAR"
        commands = [
            'message(STATUS "Special chars: $<$<CONFIG:Debug>:_DEBUG>")',
            'set(PATH "C:\\Program Files\\App")',
            'message(STATUS "Quotes: \\"inside\\" quotes")',
        ]

        # Act
        result = template.generate(condition=condition, commands=commands)

        # Assert
        expected = 'if(DEFINED MY_VAR)\n  message(STATUS "Special chars: $<$<CONFIG:Debug>:_DEBUG>")\n  set(PATH "C:\\Program Files\\App")\n  message(STATUS "Quotes: \\"inside\\" quotes")\nendif()'
        assert result == expected

    # Handle very long conditions
    def test_very_long_conditions(self):
        # Arrange
        template = CMakeIfTemplate()
        condition = "DEFINED VAR1 AND DEFINED VAR2 AND VAR1 GREATER 10 AND VAR2 LESS_EQUAL 20 AND EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/file.txt AND NOT DEFINED SOME_OTHER_VAR"
        commands = ['message(STATUS "Complex condition met")']

        # Act
        result = template.generate(condition=condition, commands=commands)

        # Assert
        expected = f'if({condition})\n  message(STATUS "Complex condition met")\nendif()'
        assert result == expected

    # Handle multiline commands in the commands list
    def test_multiline_commands(self):
        # Arrange
        template = CMakeIfTemplate()
        condition = "UNIX"
        commands = [
            'message(STATUS "First line\n  Second line\n  Third line")',
            "execute_process(COMMAND ls\n  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}\n  OUTPUT_VARIABLE LS_OUTPUT)",
        ]

        # Act
        result = template.generate(condition=condition, commands=commands)

        # Assert
        expected = 'if(UNIX)\n  message(STATUS "First line\n  Second line\n  Third line")\n  execute_process(COMMAND ls\n  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}\n  OUTPUT_VARIABLE LS_OUTPUT)\nendif()'
        assert result == expected

    # Dictionary with empty keys or values for property templates
    def test_cmake_set_property_template_empty_keys_values(self):
        template = CMakeSetPropertyTemplate()
        target = "my_target"
        properties = {"": "", "KEY": ""}
        expected_output = "set_target_properties(my_target PROPERTIES   KEY )"
        assert template.generate(target, properties) == expected_output

    # Templates with nested commands maintain proper indentation
    def test_cmake_foreach_template_nested_commands_indentation(self):
        template = CMakeForeachTemplate()
        variable = "item"
        items = ["item1", "item2"]
        commands = ['if(item STREQUAL "item1")', 'message(STATUS "Item1 found")', "endif()"]
        expected_output = (
            "foreach(item item1 item2)\n"
            '  if(item STREQUAL "item1")\n'
            '  message(STATUS "Item1 found")\n'
            "  endif()\n"
            "endforeach()"
        )
        assert template.generate(variable, items, commands) == expected_output

    # Templates preserve the exact format required by CMake syntax
    def test_cmake_project_template_format(self):
        template = CMakeProjectTemplate()
        result = template.generate("MyProject", ["CXX", "C", "ASM"])
        assert result == "project(MyProject LANGUAGES CXX C ASM)"

    # Templates with optional parameters handle default values correctly
    def test_cmake_find_library_template_default_paths(self):
        template = CMakeFindLibraryTemplate()
        result = template.generate("MyLibrary")
        assert result == "find_library(MyLibrary )"

    # Templates with multiple parameters maintain correct order of arguments
    def test_cmake_add_library_template_argument_order(self):
        template = CMakeAddLibraryTemplate()
        result = template.generate("MyLib", ["file1.cpp", "file2.cpp"], "SHARED")
        assert result == "add_library(MyLib SHARED file1.cpp file2.cpp)"

    # Project management templates like CMakeProjectTemplate generate commands with correct parentheses and spacing
    def test_cmake_project_template_generation(self):
        template = CMakeProjectTemplate()
        result = template.generate(project_name="MyProject", languages=["CXX", "C", "ASM"])
        assert result == "project(MyProject LANGUAGES CXX C ASM)"

    # Complex templates like CMakeIfTemplate properly nest and format child commands
    def test_cmake_if_template_nesting(self):
        template = CMakeIfTemplate()
        commands = ['message(STATUS "Inside if")', "set(VAR VALUE)"]
        result = template.generate(condition="VAR", commands=commands)
        expected = 'if(VAR)\n  message(STATUS "Inside if")\n  set(VAR VALUE)\nendif()'
        assert result == expected

    # Target-related templates like CMakeAddExecutableTemplate properly format target names and source lists
    def test_add_executable_template_formats_correctly(self):
        template = CMakeAddExecutableTemplate()
        result = template.generate("MyExecutable", ["main.cpp", "utils.cpp"])
        assert result == "add_executable(MyExecutable main.cpp utils.cpp)"

    # File operation templates like CMakeFileOperationsTemplate correctly structure operation arguments
    def test_file_operations_template_structures_arguments(self):
        template = CMakeFileOperationsTemplate()
        result = template.generate("COPY", ["source.txt", "destination.txt"])
        assert result == "file(COPY source.txt destination.txt)"

    # Property templates like CMakeSetPropertyTemplate properly format property key-value pairs
    def test_cmake_set_property_template_formatting(self):
        template = CMakeSetPropertyTemplate()
        properties = {"KEY1": "VALUE1", "KEY2": "VALUE2"}
        result = template.generate("MyTarget", properties)
        assert result == "set_target_properties(MyTarget PROPERTIES KEY1 VALUE1 KEY2 VALUE2)"

    # Attempting to instantiate the abstract CMakeTemplate class directly raises TypeError
    def test_abstract_class_instantiation(self):
        with pytest.raises(TypeError):
            CMakeTemplate()
