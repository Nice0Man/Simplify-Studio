import importlib
import logging
import sys
from typing import Dict, Any, List

from rich.console import Console

from modules.simplify_studio._utils.utils import discover_commands

console = Console()


def run() -> None:
    """
    Main function to run the command-line interface.
    """
    if len(sys.argv) < 2:
        console.print(
            "[bold red]Error:[/bold red] A command must be specified.", style="bold"
        )
        console.print("Use [cyan]help[/cyan] to view available commands.", style="dim")
        logging.error("No command specified.")
        sys.exit(1)

    command_name = sys.argv[1].lower()
    command_data = discover_commands()
    logging.info(f"Executing command: {command_name}")
    execute_command(command_name, command_data)


def execute_command(
    command_name: str, command_data: Dict[str, List[Dict[str, Any]]]
) -> None:
    """
    Executes the specified command by name.

    Args:
        command_name: The name of the command to execute.
        command_data: A dictionary containing command categories and their respective commands.
    """
    for module_info in command_data.get("root", []):
        category = module_info["pkg_name"]
        commands = module_info["commands"]

        for command in commands:
            if command_name == command["command_name"]:
                module_name = (
                    f"modules.simplify_studio._api._commands.{category}.{command_name}"
                )
                try:
                    module = importlib.import_module(module_name)
                    command_class = getattr(module, command_name.capitalize(), None)

                    if command_class is None:
                        raise AttributeError(
                            f"Class {command_name.capitalize()} not found in module {module_name}"
                        )

                    command_instance = command_class()
                    if command_instance.execute():
                        logging.info(f"Successfully executed command: {command_name}")
                        command_instance.format_for_cli()
                    else:
                        logging.warn(f"Command '{command_name}' executed with errors")
                    return

                except (ImportError, AttributeError) as e:
                    console.print(
                        f"[bold red]Error:[/bold red] Failed to execute command: [yellow]{command_name}[/yellow]",
                        style="bold",
                    )
                    console.print(str(e), style="dim")
                    logging.error(
                        f"Failed to execute command: {command_name}. Error: {e}"
                    )
                    return

    console.print(
        f"[bold red]Error:[/bold red] Command [yellow]{command_name}[/yellow] not found.",
        style="bold",
    )
    logging.warning(f"Command not found: {command_name}")


if __name__ == "__main__":
    run()
