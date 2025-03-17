from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    """Abstract base class for defining command objects in the system.

    Provides a standardized interface for command pattern implementation. Subclasses must
    implement the execution logic while maintaining consistent error handling.

    Methods:
        execute: Main entry point for command execution
        get_command_name: Helper method to derive command name from class name
    """

    @abstractmethod
    def execute(self, *args, **kwargs) -> bool:
        """Execute the primary command logic.

        Args:
            *args: Positional arguments for command execution
            **kwargs: Keyword arguments for command execution

        Returns:
            bool: True if command succeeded, False if failed

        Raises:
            Implementation-specific exceptions should be documented in subclasses
        """
        pass

    def get_command_name(self) -> str:
        """Generate normalized command name from class name.

        Converts PascalCase class name to lowercase identifier by removing 'Command' suffix
        if present and converting to snake_case.

        Example:
            class FileUploadCommand(Command) -> 'file_upload'

        Returns:
            str: Normalized command name in snake_case
        """
        return self.__class__.__name__.lower()


class CommandOutput(ABC):
    """Abstract base class for formatting command results to different output formats.

    Defines interface for adapting command execution results to various presentation layers
    while maintaining separation of concerns between business logic and presentation.
    """

    @abstractmethod
    def format_for_cli(self, *args, **kwargs) -> None:
        """Format command results for command-line interface output.

        Implements rich text formatting using the `rich` library for console presentation.
        Directly outputs to console rather than returning values.

        Args:
            *args: Raw command execution results
            **kwargs: Formatting options (colors, tables, progress bars, etc.)
        """
        pass

    @abstractmethod
    def format_for_web(self, *args, **kwargs) -> dict[str, Any]:
        """Serialize command results for web API responses.

        Transforms command output into JSON-serializable format following API specifications.

        Args:
            *args: Raw command execution results
            **kwargs: Serialization options (field filtering, data wrapping, etc.)

        Returns:
            dict[str, Any]: Standardized response structure with:
                - status: Operation outcome (success/error)
                - data: Processed payload
                - metadata: Additional contextual information

        Requirements:
            - Keys must use snake_case notation
            - All values must be JSON-serializable types
            - Error responses must include 'error_code' and 'message' fields
        """
        pass
