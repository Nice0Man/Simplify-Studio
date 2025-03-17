import importlib
import importlib.util
import os
import inspect
from typing import Dict, List, Any
from modules.simplify_studio._api import _commands as commands_pkg
from modules.simplify_studio._api._commands.command import Command


def get_module_description(root_path: str) -> str:
    """
    Extracts the module description from the `__init__.py` file.

    Args:
        root_path: The root path of the module.

    Returns:
        The module description if available, otherwise a default message.
    """
    init_path = os.path.join(root_path, "__init__.py")
    if os.path.exists(init_path):
        spec = importlib.util.spec_from_file_location("module_init", init_path)
        module_init = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module_init)
        return str(
            getattr(module_init, "MODULE_DESCRIPTION", "No description available.")
        )
    return "No description available."


def discover_commands() -> Dict[str, List[Dict[str, Any]]]:
    """
    Recursively discovers all available commands in the `_commands` package
    and groups them by module.

    Returns:
        A structured representation of commands grouped by module.
    """
    command_structure = {"root": []}
    base_path = commands_pkg.__path__[0]

    for root, _, files in os.walk(base_path):
        module_pkg = os.path.basename(root)
        if module_pkg == "_commands":
            continue

        module_description = get_module_description(root)
        module_data = {
            "pkg_name": module_pkg,
            "module_description": module_description,
            "commands": [],
        }

        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                module_path = os.path.relpath(os.path.join(root, file), base_path)
                module_name = module_path.replace(os.sep, ".").replace(".py", "")
                full_module_name = f"{commands_pkg.__name__}.{module_name}"

                try:
                    module = importlib.import_module(full_module_name)
                    discover_classes(module, module_data["commands"])
                except ImportError as e:
                    print(f"Could not import module {full_module_name}: {e}")

        if module_data["commands"]:
            command_structure["root"].append(module_data)

    return command_structure


def discover_classes(module: Any, commands_list: List[Dict[str, Any]]) -> None:
    """
    Finds all classes in a module that inherit from Command and adds them to the structure.

    Args:
        module: The module to inspect.
        commands_list: The list to append command information to.
    """
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, Command) and obj is not Command:
            command_info = {
                "command_name": name.lower(),
                "description": (
                    obj.__doc__.strip() if obj.__doc__ else "No description available."
                ),
                "args": get_command_arguments(obj),
            }
            commands_list.append(command_info)


def get_command_arguments(command_class: Any) -> Dict[str, str]:
    """
    Retrieves arguments for a command class if defined.

    Args:
        command_class: The command class to inspect.

    Returns:
        A dictionary of argument names and example values.
    """
    args = {}
    execute_method = getattr(command_class, "execute", None)
    if execute_method:
        sig = inspect.signature(execute_method)
        for param_name, param in sig.parameters.items():
            if param_name not in ["self", "args", "kwargs"]:
                args[param_name] = f"<{param_name}>"

    return args
