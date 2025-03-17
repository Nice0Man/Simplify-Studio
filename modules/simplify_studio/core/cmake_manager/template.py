from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class CMakeTemplate(ABC):
    """
    Abstract base class for CMake templates.

    This class serves as a blueprint for creating specific CMake command templates.
    Each subclass should implement the `generate` method to produce the appropriate
    CMake command string.
    """

    def __init__(self):
        """
        Initialize the template with a command key derived from class name.
        """
        self._command_key: str = ""

    @property
    def command_key(self) -> str:
        """
        Get the command key for the template.

        :returns: The command key as a string.
        """
        return self._command_key

    @command_key.setter
    def command_key(self, value: str):
        """
        Set the command key for the template.

        :param value: The command key to set.
        """
        self._command_key = value

    @abstractmethod
    def generate(self, **kwargs) -> str:
        """
        Generate the CMake command string.

        :param kwargs: Keyword arguments for command generation.
        :returns: Configured CMake command string.
        :raises NotImplementedError: If the method is not implemented in a subclass.
        """
        pass


# 1. Project Management and Configuration
class CMakeProjectTemplate(CMakeTemplate):
    """
    Generates a CMake project command.

    This class is responsible for creating a CMake command that defines a project
    with a specified name and the programming languages it supports.

    Example:
        project(MyProject LANGUAGES C CXX)
    """

    def __init__(self):
        """
        Initialize the CMakeProjectTemplate.

        Sets the command key to "project".
        """
        super().__init__()
        self.command_key = "project"

    def generate(self, project_name: str, languages: List[str]) -> str:
        """
        Generate the CMake project command.

        :param project_name: The name of the project.
        :param languages: A list of programming languages supported by the project.
        :returns: The generated CMake project command.
        """
        return f"{self.command_key}({project_name} LANGUAGES {' '.join(languages)})"


class CMakeMinimumRequiredTemplate(CMakeTemplate):
    """
    Generates a CMake command to set the minimum required version.

    This class generates a CMake command to specify the minimum version of CMake
    required to build the project.

    Example:
        cmake_minimum_required(VERSION 3.13)
    """

    def __init__(self):
        """
        Initialize the CMakeMinimumRequiredTemplate.

        Sets the command key to "cmake_minimum_required".
        """
        super().__init__()
        self.command_key = "cmake_minimum_required"

    def generate(self, version: str) -> str:
        """
        Generate the CMake minimum required version command.

        :param version: The minimum required version of CMake.
        :returns: The generated CMake minimum required version command.
        """
        return f"{self.command_key}(VERSION {version})"


class CMakeIncludeTemplate(CMakeTemplate):
    """
    Generates a CMake command to include an external file or module.

    This class generates a CMake command to include another CMake file or module
    into the current build configuration.

    Example:
        include(MyModule)
    """

    def __init__(self):
        """
        Initialize the CMakeIncludeTemplate.

        Sets the command key to "include".
        """
        super().__init__()
        self.command_key = "include"

    def generate(self, file: str) -> str:
        """
        Generate the CMake include command.

        :param file: The path to the file or module to include.
        :returns: The generated CMake include command.
        """
        return f"{self.command_key}({file})"


class CMakeAddSubdirectoryTemplate(CMakeTemplate):
    """
    Generates a CMake command to add a subdirectory.

    This class generates a CMake command to add a subdirectory to the build,
    allowing it to be included in the build process.

    Example:
        add_subdirectory(src)
    """

    def __init__(self):
        """
        Initialize the CMakeAddSubdirectoryTemplate.

        Sets the command key to "add_subdirectory".
        """
        super().__init__()
        self.command_key = "add_subdirectory"

    def generate(self, directory: str) -> str:
        """
        Generate the CMake add subdirectory command.

        :param directory: The path to the subdirectory to add.
        :returns: The generated CMake add subdirectory command.
        """
        return f"{self.command_key}({directory})"


class CMakeEnableLanguageTemplate(CMakeTemplate):
    """
    Generates a CMake command to enable support for specified languages.

    This class generates a CMake command to enable support for one or more
    programming languages in the project.

    Example:
        enable_language(C CXX)
    """

    def __init__(self):
        """
        Initialize the CMakeEnableLanguageTemplate.

        Sets the command key to "enable_language".
        """
        super().__init__()
        self.command_key = "enable_language"

    def generate(self, languages: List[str]) -> str:
        """
        Generate the CMake enable language command.

        :param languages: A list of programming languages to enable.
        :returns: The generated CMake enable language command.
        """
        return f"{self.command_key}({' '.join(languages)})"


class CMakeSetTemplate(CMakeTemplate):
    """
    Generates a CMake command to set a variable.

    This class generates a CMake command to set a variable to a specified value.

    Example:
        set(MY_VAR "value")
    """

    def __init__(self):
        """
        Initialize the CMakeSetTemplate.

        Sets the command key to "set".
        """
        super().__init__()
        self.command_key = "set"

    def generate(self, variable: str, value: str) -> str:
        """
        Generate the CMake set command.

        :param variable: The name of the variable to set.
        :param value: The value to assign to the variable.
        :returns: The generated CMake set command.
        """
        return f"{self.command_key}({variable} {value})"


class CMakeUnsetTemplate(CMakeTemplate):
    """
    Generates a CMake command to unset a variable.

    This class generates a CMake command to unset a previously set variable.

    Example:
        unset(MY_VAR)
    """

    def __init__(self):
        """
        Initialize the CMakeUnsetTemplate.

        Sets the command key to "unset".
        """
        super().__init__()
        self.command_key = "unset"

    def generate(self, variable: str) -> str:
        """
        Generate the CMake unset command.

        :param variable: The name of the variable to unset.
        :returns: The generated CMake unset command.
        """
        return f"{self.command_key}({variable})"


class CMakeOptionTemplate(CMakeTemplate):
    """
    Generates a CMake command to define an option.

    This class generates a CMake command to define a build option with a
    description and a default value.

    Example:
        option(BUILD_SHARED_LIBS "Build using shared libraries" ON)
    """

    def __init__(self):
        """
        Initialize the CMakeOptionTemplate.

        Sets the command key to "option".
        """
        super().__init__()
        self.command_key = "option"

    def generate(self, option: str, description: str, default: str) -> str:
        """
        Generate the CMake option command.

        :param option: The name of the option.
        :param description: A brief description of the option.
        :param default: The default value for the option.
        :returns: The generated CMake option command.
        """
        return f'{self.command_key}({option} "{description}" {default})'


# 2. Targets
class CMakeAddExecutableTemplate(CMakeTemplate):
    """
    Generates a CMake command to add an executable target.

    This class generates a CMake command to define an executable target with
    specified source files.

    Example:
        add_executable(MyExecutable main.cpp)
    """

    def __init__(self):
        """
        Initialize the CMakeAddExecutableTemplate.

        Sets the command key to "add_executable".
        """
        super().__init__()
        self.command_key = "add_executable"

    def generate(self, target_name: str, sources: List[str]) -> str:
        """
        Generate the CMake add executable command.

        :param target_name: The name of the executable target.
        :param sources: A list of source files for the executable.
        :returns: The generated CMake add executable command.
        """
        return f"{self.command_key}({target_name} {' '.join(sources)})"


class CMakeAddLibraryTemplate(CMakeTemplate):
    """
    Generates a CMake command to add a library target.

    This class generates a CMake command to define a library target with
    specified source files and library type.

    Example:
        add_library(MyLibrary STATIC mylib.cpp)
    """

    def __init__(self):
        """
        Initialize the CMakeAddLibraryTemplate.

        Sets the command key to "add_library".
        """
        super().__init__()
        self.command_key = "add_library"

    def generate(self, lib_name: str, sources: List[str], lib_type: str = "STATIC") -> str:
        """
        Generate the CMake add library command.

        :param lib_name: The name of the library target.
        :param sources: A list of source files for the library.
        :param lib_type: The type of library (e.g., STATIC, SHARED). Defaults to "STATIC".
        :returns: The generated CMake add library command.
        """
        return f"{self.command_key}({lib_name} {lib_type} {' '.join(sources)})"


class CMakeAddCustomTargetTemplate(CMakeTemplate):
    """
    Generates a CMake command to add a custom target.

    This class generates a CMake command to define a custom target with a
    specified command.

    Example:
        add_custom_target(MyTarget ALL COMMAND echo "Hello, World!")
    """

    def __init__(self):
        """
        Initialize the CMakeAddCustomTargetTemplate.

        Sets the command key to "add_custom_target".
        """
        super().__init__()
        self.command_key = "add_custom_target"

    def generate(self, target_name: str, command: str) -> str:
        """
        Generate the CMake add custom target command.

        :param target_name: The name of the custom target.
        :param command: The command to execute for the custom target.
        :returns: The generated CMake add custom target command.
        """
        return f"{self.command_key}({target_name} {command})"


class CMakeTargetSourcesTemplate(CMakeTemplate):
    """
    Generates a CMake command to add sources to a target.

    This class generates a CMake command to add source files to an existing
    target.

    Example:
        target_sources(MyTarget PRIVATE source1.cpp source2.cpp)
    """

    def __init__(self):
        """
        Initialize the CMakeTargetSourcesTemplate.

        Sets the command key to "target_sources".
        """
        super().__init__()
        self.command_key = "target_sources"

    def generate(self, target_name: str, sources: List[str]) -> str:
        """
        Generate the CMake target sources command.

        :param target_name: The name of the target.
        :param sources: A list of source files to add to the target.
        :returns: The generated CMake target sources command.
        """
        return f"{self.command_key}({target_name} PRIVATE {' '.join(sources)})"


class CMakeTargetIncludeDirectoriesTemplate(CMakeTemplate):
    """
    Generates a CMake command to specify include directories for a target.

    This class generates a CMake command to specify include directories for
    an existing target.

    Example:
        target_include_directories(MyTarget PRIVATE include/)
    """

    def __init__(self):
        """
        Initialize the CMakeTargetIncludeDirectoriesTemplate.

        Sets the command key to "target_include_directories".
        """
        super().__init__()
        self.command_key = "target_include_directories"

    def generate(self, target_name: str, directories: List[str]) -> str:
        """
        Generate the CMake target include directories command.

        :param target_name: The name of the target.
        :param directories: A list of include directories for the target.
        :returns: The generated CMake target include directories command.
        """
        return f"{self.command_key}({target_name} PRIVATE {' '.join(directories)})"


class CMakeTargetCompileDefinitionsTemplate(CMakeTemplate):
    """
    Generates a CMake command to define compile-time macros for a target.

    This class generates a CMake command to define compile-time macros for
    an existing target.

    Example:
        target_compile_definitions(MyTarget PRIVATE MY_MACRO=1)
    """

    def __init__(self):
        """
        Initialize the CMakeTargetCompileDefinitionsTemplate.

        Sets the command key to "target_compile_definitions".
        """
        super().__init__()
        self.command_key = "target_compile_definitions"

    def generate(self, target_name: str, definitions: List[str]) -> str:
        """
        Generate the CMake target compile definitions command.

        :param target_name: The name of the target.
        :param definitions: A list of compile-time macros for the target.
        :returns: The generated CMake target compile definitions command.
        """
        return f"{self.command_key}({target_name} PRIVATE {' '.join(definitions)})"


class CMakeTargetCompileOptionsTemplate(CMakeTemplate):
    """
    Generates a CMake command to set compile options for a target.

    This class generates a CMake command to set compile options for an
    existing target.

    Example:
        target_compile_options(MyTarget PRIVATE -Wall -Wextra)
    """

    def __init__(self):
        """
        Initialize the CMakeTargetCompileOptionsTemplate.

        Sets the command key to "target_compile_options".
        """
        super().__init__()
        self.command_key = "target_compile_options"

    def generate(self, target_name: str, options: List[str]) -> str:
        """
        Generate the CMake target compile options command.

        :param target_name: The name of the target.
        :param options: A list of compile options for the target.
        :returns: The generated CMake target compile options command.
        """
        return f"{self.command_key}({target_name} PRIVATE {' '.join(options)})"


class CMakeTargetLinkLibrariesTemplate(CMakeTemplate):
    """
    Generates a CMake command to link libraries to a target.

    This class generates a CMake command to link libraries to an existing
    target.

    Example:
        target_link_libraries(MyTarget PRIVATE MyLibrary)
    """

    def __init__(self):
        """
        Initialize the CMakeTargetLinkLibrariesTemplate.

        Sets the command key to "target_link_libraries".
        """
        super().__init__()
        self.command_key = "target_link_libraries"

    def generate(self, target_name: str, libraries: List[str]) -> str:
        """
        Generate the CMake target link libraries command.

        :param target_name: The name of the target.
        :param libraries: A list of libraries to link to the target.
        :returns: The generated CMake target link libraries command.
        """
        return f"{self.command_key}({target_name} {' '.join(libraries)})"


class CMakeTargetLinkDirectoriesTemplate(CMakeTemplate):
    """
    Generates a CMake command to specify link directories for a target.

    This class generates a CMake command to specify link directories for
    an existing target.

    Example:
        target_link_directories(MyTarget PRIVATE lib/)
    """

    def __init__(self):
        """
        Initialize the CMakeTargetLinkDirectoriesTemplate.

        Sets the command key to "target_link_directories".
        """
        super().__init__()
        self.command_key = "target_link_directories"

    def generate(self, target_name: str, directories: List[str]) -> str:
        """
        Generate the CMake target link directories command.

        :param target_name: The name of the target.
        :param directories: A list of link directories for the target.
        :returns: The generated CMake target link directories command.
        """
        return f"{self.command_key}({target_name} PRIVATE {' '.join(directories)})"


class CMakeTargetLinkOptionsTemplate(CMakeTemplate):
    """
    Generates a CMake command to set link options for a target.

    This class generates a CMake command to set link options for an
    existing target.

    Example:
        target_link_options(MyTarget PRIVATE -Wl,--no-undefined)
    """

    def __init__(self):
        """
        Initialize the CMakeTargetLinkOptionsTemplate.

        Sets the command key to "target_link_options".
        """
        super().__init__()
        self.command_key = "target_link_options"

    def generate(self, target_name: str, options: List[str]) -> str:
        """
        Generate the CMake target link options command.

        :param target_name: The name of the target.
        :param options: A list of link options for the target.
        :returns: The generated CMake target link options command.
        """
        return f"{self.command_key}({target_name} PRIVATE {' '.join(options)})"


# 3. File and Directory Operations
class CMakeFileOperationsTemplate(CMakeTemplate):
    """
    Generates a CMake command for file operations.

    This class generates a CMake command to perform operations on files,
    such as copying, removing, or reading file properties.

    Example:
        file(COPY source DESTINATION destination)
    """

    def __init__(self):
        """
        Initialize the CMakeFileOperationsTemplate.

        Sets the command key to "file".
        """
        super().__init__()
        self.command_key = "file"

    def generate(self, operation: str, args: List[str]) -> str:
        """
        Generate the CMake file operations command.

        :param operation: The file operation to perform (e.g., COPY, REMOVE).
        :param args: A list of arguments for the file operation.
        :returns: The generated CMake file operations command.
        """
        return f"{self.command_key}({operation} {' '.join(args)})"


class CMakeConfigureFileTemplate(CMakeTemplate):
    """
    Generates a CMake command to configure a file.

    This class generates a CMake command to configure a file by replacing
    variables with their values.

    Example:
        configure_file(input.txt output.txt)
    """

    def __init__(self):
        """
        Initialize the CMakeConfigureFileTemplate.

        Sets the command key to "configure_file".
        """
        super().__init__()
        self.command_key = "configure_file"

    def generate(self, input_file: str, output_file: str) -> str:
        """
        Generate the CMake configure file command.

        :param input_file: The input file to configure.
        :param output_file: The output file to generate.
        :returns: The generated CMake configure file command.
        """
        return f"{self.command_key}({input_file} {output_file})"


class CMakeFindFileTemplate(CMakeTemplate):
    """
    Generates a CMake command to find a file.

    This class generates a CMake command to locate a file in the specified
    paths.

    Example:
        find_file(MY_FILE myfile.txt PATHS /usr/local)
    """

    def __init__(self):
        """
        Initialize the CMakeFindFileTemplate.

        Sets the command key to "find_file".
        """
        super().__init__()
        self.command_key = "find_file"

    def generate(self, file_name: str, paths: Optional[List[str]] = None) -> str:
        """
        Generate the CMake find file command.

        :param file_name: The name of the file to find.
        :param paths: Optional list of paths to search for the file.
        :returns: The generated CMake find file command.
        """
        paths_str = " ".join(paths) if paths else ""
        return f"{self.command_key}({file_name} {paths_str})"


class CMakeFindLibraryTemplate(CMakeTemplate):
    """
    Generates a CMake command to find a library.

    This class generates a CMake command to locate a library in the specified
    paths.

    Example:
        find_library(MY_LIB mylib PATHS /usr/local/lib)
    """

    def __init__(self):
        """
        Initialize the CMakeFindLibraryTemplate.

        Sets the command key to "find_library".
        """
        super().__init__()
        self.command_key = "find_library"

    def generate(self, library_name: str, paths: Optional[List[str]] = None) -> str:
        """
        Generate the CMake find library command.

        :param library_name: The name of the library to find.
        :param paths: Optional list of paths to search for the library.
        :returns: The generated CMake find library command.
        """
        paths_str = " ".join(paths) if paths else ""
        return f"{self.command_key}({library_name} {paths_str})"


class CMakeListOperationsTemplate(CMakeTemplate):
    """
    Generates a CMake command for list operations.

    This class generates a CMake command to perform operations on lists,
    such as APPEND, REMOVE, or SORT.

    Example:
        list(APPEND mylist item1 item2)
    """

    def __init__(self):
        """
        Initialize the CMakeListOperationsTemplate.

        Sets the command key to "list".
        """
        super().__init__()
        self.command_key = "list"

    def generate(self, operation: str, list_name: str, values: List[str]) -> str:
        """
        Generate the CMake list operations command.

        :param operation: The list operation to perform (e.g., APPEND, REMOVE).
        :param list_name: The name of the list to operate on.
        :param values: A list of values for the list operation.
        :returns: The generated CMake list operations command.
        """
        return f"{self.command_key}({operation} {list_name} {' '.join(values)})"


class CMakeGetFilenameComponentTemplate(CMakeTemplate):
    """
    Generates a CMake command to get a filename component.

    This class generates a CMake command to extract a component from a
    filename, such as the directory, name, or extension.

    Example:
        get_filename_component(DIR myfile.txt DIRECTORY)
    """

    def __init__(self):
        """
        Initialize the CMakeGetFilenameComponentTemplate.

        Sets the command key to "get_filename_component".
        """
        super().__init__()
        self.command_key = "get_filename_component"

    def generate(self, variable: str, filename: str, component: str) -> str:
        """
        Generate the CMake get filename component command.

        :param variable: The variable to store the extracted component.
        :param filename: The filename to extract the component from.
        :param component: The component to extract (e.g., DIRECTORY, NAME).
        :returns: The generated CMake get filename component command.
        """
        return f"{self.command_key}({variable} {filename} {component})"


# 4. Property Management
class CMakeSetPropertyTemplate(CMakeTemplate):
    """
    Generates a CMake command to set properties for a target.

    This class generates a CMake command to set properties for a target,
    such as its version or output name.

    Example:
        set_target_properties(MyTarget PROPERTIES VERSION 1.0)
    """

    def __init__(self):
        """
        Initialize the CMakeSetPropertyTemplate.

        Sets the command key to "set_target_properties".
        """
        super().__init__()
        self.command_key = "set_target_properties"

    def generate(self, target: str, properties: Dict[str, str]) -> str:
        """
        Generate the CMake set property command.

        :param target: The name of the target to set properties for.
        :param properties: A dictionary of properties and their values.
        :returns: The generated CMake set property command.
        """
        return f"{self.command_key}({target} PROPERTIES {' '.join([f'{key} {value}' for key, value in properties.items()])})"


class CMakeGetPropertyTemplate(CMakeTemplate):
    """
    Generates a CMake command to retrieve property values.

    This class generates a CMake command to retrieve the value of a property
    for a target or directory.

    Example:
        get_property(VALUE MyTarget PROPERTY VERSION)
    """

    def __init__(self):
        """
        Initialize the CMakeGetPropertyTemplate.

        Sets the command key to "get_property".
        """
        super().__init__()
        self.command_key = "get_property"

    def generate(self, variable: str, target: str, property_name: str) -> str:
        """
        Generate the CMake get property command.

        :param variable: The variable to store the property value.
        :param target: The name of the target or directory.
        :param property_name: The name of the property to retrieve.
        :returns: The generated CMake get property command.
        """
        return f"{self.command_key}({variable} {target} {property_name})"


class CMakeDefinePropertyTemplate(CMakeTemplate):
    """
    Generates a CMake command to define properties.

    This class generates a CMake command to define a new property with
    specified attributes.

    Example:
        define_property(TARGET MyProperty BRIEF_DOCS "A custom property")
    """

    def __init__(self):
        """
        Initialize the CMakeDefinePropertyTemplate.

        Sets the command key to "define_property".
        """
        super().__init__()
        self.command_key = "define_property"

    def generate(self, property_name: str, scope: str, attributes: Dict[str, str]) -> str:
        """
        Generate the CMake define property command.

        :param property_name: The name of the property to define.
        :param scope: The scope of the property (e.g., TARGET, DIRECTORY).
        :param attributes: A dictionary of attributes for the property.
        :returns: The generated CMake define property command.
        """
        attributes_str = " ".join([f'{key} "{value}"' for key, value in attributes.items()])
        return f"{self.command_key}({property_name} {scope} {attributes_str})"


class CMakeSetDirectoryPropertiesTemplate(CMakeTemplate):
    """
    Generates a CMake command to set directory properties.

    This class generates a CMake command to set properties for a directory,
    such as its include directories or compile options.

    Example:
        set_directory_properties(PROPERTIES INCLUDE_DIRECTORIES include/)
    """

    def __init__(self):
        """
        Initialize the CMakeSetDirectoryPropertiesTemplate.

        Sets the command key to "set_directory_properties".
        """
        super().__init__()
        self.command_key = "set_directory_properties"

    def generate(self, properties: Dict[str, str]) -> str:
        """
        Generate the CMake set directory properties command.

        :param properties: A dictionary of properties and their values.
        :returns: The generated CMake set directory properties command.
        """
        properties_str = " ".join([f"{key} {value}" for key, value in properties.items()])
        return f"{self.command_key}(PROPERTIES {properties_str})"


# 5. Conditional Logic and Control Flow
class CMakeIfTemplate(CMakeTemplate):
    """
    Generates a CMake command for conditional logic using the IF, ELSEIF, ELSE, and ENDIF blocks.

    This class generates a CMake command to perform conditional logic using
    the IF, ELSEIF, ELSE, and ENDIF blocks.

    Example:
        if(CONDITION)
          # Commands
        endif()
    """

    def __init__(self):
        """
        Initialize the CMakeIfTemplate.

        Sets the command key to "if".
        """
        super().__init__()
        self.command_key = "if"

    def generate(self, condition: str, commands: List[str]) -> str:
        """
        Generate the CMake if command.

        :param condition: The condition to evaluate.
        :param commands: A list of commands to execute if the condition is true.
        :returns: The generated CMake if command.
        """
        indented_commands = "\n  ".join(commands)  # Add indentation
        return f"{self.command_key}({condition})\n  {indented_commands}\nendif()"


class CMakeElseIfTemplate(CMakeTemplate):
    """
    Generates a CMake command for ELSEIF logic.

    This class generates a CMake command to perform ELSEIF logic within
    an IF block.

    Example:
        elseif(CONDITION)
    """

    def __init__(self):
        """
        Initialize the CMakeElseIfTemplate.

        Sets the command key to "elseif".
        """
        super().__init__()
        self.command_key = "elseif"

    def generate(self, condition: str) -> str:
        """
        Generate the CMake elseif command.

        :param condition: The condition to evaluate.
        :returns: The generated CMake elseif command.
        """
        return f"{self.command_key}({condition})"


class CMakeElseTemplate(CMakeTemplate):
    """
    Generates a CMake command for ELSE logic.

    This class generates a CMake command to perform ELSE logic within
    an IF block.

    Example:
        else()
    """

    def __init__(self):
        """
        Initialize the CMakeElseTemplate.

        Sets the command key to "else".
        """
        super().__init__()
        self.command_key = "else"

    def generate(self) -> str:
        """
        Generate the CMake else command.

        :returns: The generated CMake else command.
        """
        return f"{self.command_key}()"


class CMakeWhileTemplate(CMakeTemplate):
    """
    Generates a CMake command for WHILE loops.

    This class generates a CMake command to perform a WHILE loop with
    specified commands.

    Example:
        while(CONDITION)
          # Commands
        endwhile()
    """

    def __init__(self):
        """
        Initialize the CMakeWhileTemplate.

        Sets the command key to "while".
        """
        super().__init__()
        self.command_key = "while"

    def generate(self, condition: str, commands: List[str]) -> str:
        """
        Generate the CMake while command.

        :param condition: The condition to evaluate for the loop.
        :param commands: A list of commands to execute within the loop.
        :returns: The generated CMake while command.
        """
        indented_commands = "\n  ".join(commands)
        return f"{self.command_key}({condition})\n  {indented_commands}\nendwhile()"


class CMakeForeachTemplate(CMakeTemplate):
    """
    Generates a CMake command for looping over a list.

    This class generates a CMake command to perform a FOREACH loop over
    a list of items.

    Example:
        foreach(VAR IN ITEMS item1 item2)
          # Commands
        endforeach()
    """

    def __init__(self):
        """
        Initialize the CMakeForeachTemplate.

        Sets the command key to "foreach".
        """
        super().__init__()
        self.command_key = "foreach"

    def generate(self, variable: str, items: List[str], commands: List[str]) -> str:
        """
        Generate the CMake foreach command.

        :param variable: The loop variable name.
        :param items: A list of items to iterate over.
        :param commands: A list of commands to execute within the loop.
        :returns: The generated CMake foreach command.
        """
        indented_commands = "\n  ".join(commands)  # Add indentation
        return (
            f"{self.command_key}({variable} {' '.join(items)})\n  {indented_commands}\nendforeach()"
        )


class CMakeBreakTemplate(CMakeTemplate):
    """
    Generates a CMake command to break loops.

    This class generates a CMake command to break out of a loop.

    Example:
        break()
    """

    def __init__(self):
        """
        Initialize the CMakeBreakTemplate.

        Sets the command key to "break".
        """
        super().__init__()
        self.command_key = "break"

    def generate(self) -> str:
        """
        Generate the CMake break command.

        :returns: The generated CMake break command.
        """
        return f"{self.command_key}()"


class CMakeReturnTemplate(CMakeTemplate):
    """
    Generates a CMake command to return from a macro or function.

    This class generates a CMake command to return from a macro or function.

    Example:
        return()
    """

    def __init__(self):
        """
        Initialize the CMakeReturnTemplate.

        Sets the command key to "return".
        """
        super().__init__()
        self.command_key = "return"

    def generate(self) -> str:
        """
        Generate the CMake return command.

        :returns: The generated CMake return command.
        """
        return f"{self.command_key}()"


# 6. Testing
class CMakeEnableTestingTemplate(CMakeTemplate):
    """
    Generates a CMake command to enable testing.

    This class generates a CMake command to enable testing capabilities
    in the project.

    Example:
        enable_testing()
    """

    def __init__(self):
        """
        Initialize the CMakeEnableTestingTemplate.

        Sets the command key to "enable_testing".
        """
        super().__init__()
        self.command_key = "enable_testing"

    def generate(self) -> str:
        """
        Generate the CMake enable testing command.

        :returns: The generated CMake enable testing command.
        """
        return f"{self.command_key}()"


class CMakeAddTestTemplate(CMakeTemplate):
    """
    Generates the CMake add test command.

    This class generates a CMake command to add a test to the project.

    Example:
        add_test(NAME MyTest COMMAND my_test_executable)
    """

    def __init__(self):
        """
        Initialize the CMakeAddTestTemplate.

        Sets the command key to "add_test".
        """
        super().__init__()
        self.command_key = "add_test"

    def generate(self, test_name: str, command: str) -> str:
        """
        Generate the CMake add test command.

        :param test_name: The name of the test.
        :param command: The command to execute for the test.
        :returns: The generated CMake add test command.
        """
        return f"{self.command_key}({test_name} {command})"


class CMakeCTestTemplate(CMakeTemplate):
    """
    Generates a CMake command to enable CTest.

    This class generates a CMake command to enable CTest capabilities
    in the project.

    Example:
        ctest()
    """

    def __init__(self):
        """
        Initialize the CMakeCTestTemplate.

        Sets the command key to "ctest".
        """
        super().__init__()
        self.command_key = "ctest"

    def generate(self, options: Optional[List[str]] = None) -> str:
        """
        Generate the CMake ctest command.

        :param options: Optional list of options for the ctest command.
        :returns: The generated CMake ctest command.
        """
        options_str = " ".join(options) if options else ""
        return f"{self.command_key}({options_str})"


# 7. Installation
class CMakeInstallTemplate(CMakeTemplate):
    """
    Generates a CMake command to install targets or files.

    This class generates a CMake command to specify installation rules
    for targets or files.

    Example:
        install(TARGETS MyTarget DESTINATION /usr/local/bin)
    """

    def __init__(self):
        """
        Initialize the CMakeInstallTemplate.

        Sets the command key to "install".
        """
        super().__init__()
        self.command_key = "install"

    def generate(self, target: str, destination: str) -> str:
        """
        Generate the CMake install command.

        :param target: The name of the target to install.
        :param destination: The destination directory for the installation.
        :returns: The generated CMake install command.
        """
        return f"{self.command_key}(TARGETS {target} DESTINATION {destination})"


# 8. Packaging
class CMakeIncludeCPackTemplate(CMakeTemplate):
    """
    Generates a CMake command to include CPack.

    This class generates a CMake command to include CPack for packaging
    the project.

    Example:
        include(CPack)
    """

    def __init__(self):
        """
        Initialize the CMakeIncludeCPackTemplate.

        Sets the command key to "include(CPack)".
        """
        super().__init__()
        self.command_key = "include(CPack)"

    def generate(self) -> str:
        """
        Generate the CMake include CPack command.

        :returns: The generated CMake include CPack command.
        """
        return f"{self.command_key}"


class CMakeCpackAddComponentTemplate(CMakeTemplate):
    """
    Generates a CMake command to add a CPack component.

    This class generates a CMake command to add a component for CPack
    packaging.

    Example:
        cpack_add_component(MyComponent DISPLAY_NAME "My Component")
    """

    def __init__(self):
        """
        Initialize the CMakeCpackAddComponentTemplate.

        Sets the command key to "cpack_add_component".
        """
        super().__init__()
        self.command_key = "cpack_add_component"

    def generate(self, component_name: str, options: Dict[str, str]) -> str:
        """
        Generate the CMake cpack add component command.

        :param component_name: The name of the component to add.
        :param options: A dictionary of options for the component.
        :returns: The generated CMake cpack add component command.
        """
        options_str = " ".join([f"{key} {value}" for key, value in options.items()])
        return f"{self.command_key}({component_name} {options_str})"


# 9. Process Execution
class CMakeExecuteProcessTemplate(CMakeTemplate):
    """
    Generates a CMake command to execute a process.

    This class generates a CMake command to execute a process with
    specified commands.

    Example:
        execute_process(COMMAND my_executable)
    """

    def __init__(self):
        """
        Initialize the CMakeExecuteProcessTemplate.

        Sets the command key to "execute_process".
        """
        super().__init__()
        self.command_key = "execute_process"

    def generate(self, commands: List[str]) -> str:
        """
        Generate the CMake execute process command.

        :param commands: A list of commands to execute.
        :returns: The generated CMake execute process command.
        """
        commands_str = " ".join(commands)
        return f"{self.command_key}(COMMAND {commands_str})"


# 10. String and Math Operations
class CMakeStringOperationsTemplate(CMakeTemplate):
    """
    Generates a CMake command for string operations.

    This class generates a CMake command to perform operations on strings,
    such as CONCAT, REPLACE, etc.

    Example:
        string(CONCAT result "Hello, " "World!")
    """

    def __init__(self):
        """
        Initialize the CMakeStringOperationsTemplate.

        Sets the command key to "string".
        """
        super().__init__()
        self.command_key = "string"

    def generate(self, operation: str, args: List[str]) -> str:
        """
        Generate the CMake string operations command.

        :param operation: The string operation to perform (e.g., CONCAT, REPLACE).
        :param args: A list of arguments for the string operation.
        :returns: The generated CMake string operations command.
        """
        return f"{self.command_key}({operation} {' '.join(args)})"


class CMakeMathOperationsTemplate(CMakeTemplate):
    """
    Generates a CMake command for math operations.

    This class generates a CMake command to perform mathematical operations.

    Example:
        math(EXPR result "5 + 3")
    """

    def __init__(self):
        """
        Initialize the CMakeMathOperationsTemplate.

        Sets the command key to "math".
        """
        super().__init__()
        self.command_key = "math"

    def generate(self, operation: str, args: List[str]) -> str:
        """
        Generate the CMake math operations command.

        :param operation: The math operation to perform (e.g., EXPR).
        :param args: A list of arguments for the math operation.
        :returns: The generated CMake math operations command.
        """
        return f"{self.command_key}({operation} {' '.join(args)})"


# 11. Custom Commands
class CMakeAddCustomCommandTemplate(CMakeTemplate):
    """
    Generates a CMake command to add a custom command.

    This class generates a CMake command to add a custom command to a target.

    Example:
        add_custom_command(TARGET MyTarget COMMAND echo "Hello, World!")
    """

    def __init__(self):
        """
        Initialize the CMakeAddCustomCommandTemplate.

        Sets the command key to "add_custom_command".
        """
        super().__init__()
        self.command_key = "add_custom_command"

    def generate(self, target: str, command: str) -> str:
        """
        Generate the CMake add custom command.

        :param target: The name of the target to add the custom command to.
        :param command: The command to execute.
        :returns: The generated CMake add custom command.
        """
        return f"{self.command_key}(TARGET {target} COMMAND {command})"


# 12. Miscellaneous
class CMakeFindPackageTemplate(CMakeTemplate):
    """
    Generates a CMake command to find and include packages.

    This class generates a CMake command to find and include external
    packages.

    Example:
        find_package(MyPackage REQUIRED)
    """

    def __init__(self):
        """
        Initialize the CMakeFindPackageTemplate.

        Sets the command key to "find_package".
        """
        super().__init__()
        self.command_key = "find_package"

    def generate(self, package_name: str, required: bool = False) -> str:
        """
        Generate the CMake find package command.

        :param package_name: The name of the package to find.
        :param required: Whether the package is required. Defaults to False.
        :returns: The generated CMake find package command.
        """
        required_str = " REQUIRED" if required else ""
        return f"{self.command_key}({package_name}{required_str})"


class CMakePkgCheckModulesTemplate(CMakeTemplate):
    """
    Generates a CMake command to check for pkg-config modules.

    This class generates a CMake command to check for the presence of
    pkg-config modules.

    Example:
        pkg_check_modules(MY_MODULES REQUIRED mymodule)
    """

    def __init__(self):
        """
        Initialize the CMakePkgCheckModulesTemplate.

        Sets the command key to "pkg_check_modules".
        """
        super().__init__()
        self.command_key = "pkg_check_modules"

    def generate(self, prefix: str, modules: List[str]) -> str:
        """
        Generate the CMake pkg check modules command.

        :param prefix: The prefix for the pkg-config modules.
        :param modules: A list of pkg-config modules to check.
        :returns: The generated CMake pkg check modules command.
        """
        return f"{self.command_key}({prefix} {' '.join(modules)})"


class CMakeExportTemplate(CMakeTemplate):
    """
    Generates a CMake command to export targets.

    This class generates a CMake command to export targets for use in
    other projects.

    Example:
        export(EXPORT MyTargets)
    """

    def __init__(self):
        """
        Initialize the CMakeExportTemplate.

        Sets the command key to "export".
        """
        super().__init__()
        self.command_key = "export"

    def generate(self, export_name: str) -> str:
        """
        Generate the CMake export command.

        :param export_name: The name of the export set.
        :returns: The generated CMake export command.
        """
        return f"{self.command_key}({export_name})"


class CMakeIncludeGuardTemplate(CMakeTemplate):
    """
    Generates a CMake command for include guards.

    This class generates a CMake command to prevent multiple inclusions
    of the same file.

    Example:
        include_guard(UUID "unique-identifier")
    """

    def __init__(self):
        """
        Initialize the CMakeIncludeGuardTemplate.

        Sets the command key to "include_guard".
        """
        super().__init__()
        self.command_key = "include_guard"

    def generate(self, uuid: Optional[str] = None) -> str:
        """
        Generate the CMake include guard command.

        :param uuid: Optional UUID for the include guard.
        :returns: The generated CMake include guard command.
        """
        uuid_str = f" UUID {uuid}" if uuid else ""
        return f"{self.command_key}(){uuid_str}"


class CMakeMessageTemplate(CMakeTemplate):
    """
    Generates a CMake command for displaying messages.

    This class generates a CMake command to display messages during
    the build process.

    Example:
        message(STATUS "Building project")
    """

    def __init__(self):
        """
        Initialize the CMakeMessageTemplate.

        Sets the command key to "message".
        """
        super().__init__()
        self.command_key = "message"

    def generate(self, message_type: str, message: str) -> str:
        """
        Generate the CMake message command.

        :param message_type: The type of message (e.g., STATUS, WARNING).
        :param message: The message to display.
        :returns: The generated CMake message command.
        """
        return f'{self.command_key}({message_type} "{message}")'
