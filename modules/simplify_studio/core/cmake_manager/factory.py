from inspect import isabstract
from typing import Type, Dict

from modules.simplify_studio.core.cmake_manager import template
from modules.simplify_studio.core.cmake_manager.template import CMakeTemplate


class CMakeCommand:
    """
    Abstract base class for CMake commands.

    This class defines a common interface for all CMake command classes.
    Subclasses must implement the __str__ method to generate the CMake command string.
    """

    def __init__(self, *args, **kwargs):
        pass

    def __str__(self) -> str:
        """
        Generate the CMake command string.

        :return: str - The CMake command string.
        """
        pass


class CMakeCommandFactory:
    """
    Factory for creating CMake command objects using automatic registry pattern.
    """

    _command_registry: Dict[str, Type[CMakeTemplate]] = {}

    @classmethod
    def register_commands(cls):
        """
        Register all command classes from the template module.
        """
        for name in dir(template):
            obj = getattr(template, name)
            if (
                isinstance(obj, type)
                and not isabstract(obj)
                and issubclass(obj, CMakeTemplate)
                and hasattr(obj, "command_key")  # Ensure it's not abstract
            ):
                cls._command_registry[obj().command_key] = obj

    @classmethod
    def create_command(cls, command_key: str, **kwargs) -> str:
        """
        Create a CMake command instance using registered command classes.

        :param command_key: Key identifier for CMake command
        :param kwargs: Keyword arguments for command constructor
        :returns: Configured CMake command instance
        :raises ValueError: For unregistered command keys
        """
        if template_class := cls._command_registry.get(command_key):
            template_instance = template_class().generate(**kwargs)
            return template_instance

        available = ", ".join(cls._command_registry.keys())
        raise ValueError(f"Unknown command key: {command_key}. Available commands: {available}")
