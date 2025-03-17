import logging
import textwrap
from typing import Any, Dict

from rich.panel import Panel
from rich.text import Text

from modules.simplify_studio.api.cli.cli import console
from modules.simplify_studio.api.commands.command import Command, CommandOutput
from modules.simplify_studio.utils import utils


class Help(Command, CommandOutput):
    """Display a list of available commands with descriptions in multiple formats.

    This command provides help information for both CLI and web interfaces by:
    - Discovering available commands
    - Formatting output for different presentation layers
    - Handling command execution errors gracefully
    """

    __execution_result: Dict[str, Any] = None

    def format_for_cli(self, *args, **kwargs) -> None:
        """Format the command output for terminal display using Rich.

        Creates a panel-formatted output with:
        - Module descriptions in dimmed text
        - Command names in green
        - Command descriptions in white

        Args:
            *args: Positional arguments (not currently used)
            **kwargs: Keyword arguments (not currently used)
        """
        output = Text()

        for module_info in self.__execution_result.get("commands", []):
            module_desc = Text(
                f"\n{module_info['module_description']}\n", style="dim bold"
            )
            output.append(module_desc)

            for command in module_info["commands"]:
                cmd_name = Text(f"{command['command_name']:20}", style="green")
                description = command["description"]

                # Разбиваем описание на строки с сохранением оригинальных отступов
                desc_lines = []
                for line in description.split("\n"):
                    # Определяем исходный отступ для каждой строки
                    stripped_line = line.lstrip()
                    original_indent = " " * (len(line) - len(stripped_line))

                    # Форматируем каждую строку отдельно
                    wrapped_lines = textwrap.wrap(
                        stripped_line,
                        width=60,
                        initial_indent=original_indent,
                        subsequent_indent=original_indent,
                    )
                    desc_lines.extend(wrapped_lines or [""])

                # Собираем форматированный текст
                formatted_desc = Text("\n").join(
                    [
                        Text.assemble(
                            Text(" " * 20) if i > 0 else cmd_name,
                            Text("│ ", style="dim") if i == 0 else Text("   "),
                            Text(line, style="white"),
                        )
                        for i, line in enumerate(desc_lines)
                    ]
                )

                output.append(formatted_desc)
                output.append("\n")

            output.append(Text("─" * 90, style="dim"))
            output.append("\n")

        panel = Panel(
            output,
            title="[bold blue]Available commands[/bold blue]",
            border_style="blue",
            padding=(1, 4),
            width=100,
        )
        console.print(panel)

    def format_for_web(self, *args, **kwargs) -> Dict[str, Any]:
        """Format the command output for web API consumption.

        Returns:
            Dict[str, Any]: Standardized web response format containing:
                - status: Execution status indicator ("success"/"error")
                - data: Processed command data in structured format

        Example:
            {
                "status": "success",
                "data": {
                    "commands": [
                        {
                            "pkg_name": "_bo",
                            "module_description": "Build operations",
                            "commands": [...],
                        }
                    ]
                }
            }
        """
        return {"status": "success", "data": self.__execution_result}

    def execute(self, *args, **kwargs) -> bool:
        """Execute the help command workflow.

        Handles:
        1. Command discovery through utility functions
        2. Data processing and sanitization
        3. Error handling and logging

        Args:
            *args: Positional arguments (not currently used)
            **kwargs: Keyword arguments (not currently used)

        Returns:
            bool: True if execution succeeded, False otherwise

        Raises:
            Logs exceptions to warning channel but doesn't propagate them
        """
        try:
            command_data = utils.discover_commands()
            trimmed_data = self._trim_command_data(command_data)
            self.__execution_result = trimmed_data
            return True
        except Exception as ex:
            logging.warning(f"Failed to execute Help command: {ex}")
            return False

    @staticmethod
    def _trim_command_data(command_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize and structure raw command data for presentation.

        Filters out internal implementation details while preserving:
        - Package/module names
        - Command metadata
        - User-facing descriptions

        Args:
            command_data: Raw command data dictionary containing:
                - root: List of module dictionaries with full command details

        Returns:
            Dict[str, Any]: Sanitized data structure containing:
                - commands: List of processed module entries with:
                    - pkg_name: Package identifier
                    - module_description: Human-readable module purpose
                    - commands: List of simplified command entries
        """
        trimmed_data = {"commands": []}
        for module_info in command_data.get("root", []):
            trimmed_module_info = {
                "pkg_name": module_info["pkg_name"],
                "module_description": module_info["module_description"],
                "commands": [
                    {
                        "command_name": command["command_name"],
                        "description": command["description"],
                    }
                    for command in module_info["commands"]
                ],
            }
            trimmed_data["commands"].append(trimmed_module_info)
        return trimmed_data
