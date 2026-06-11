from pathlib import Path

from tools.text_utils import is_path_ignored, load_pathignore_patterns


def list_files(directory: str = ".") -> list[str]:
    path = Path(directory)

    if not path.exists():
        return [f"Directory does not exist: {directory}"]

    if not path.is_dir():
        return [f"Path is not a directory: {directory}"]

    items = []
    ignored_patterns = load_pathignore_patterns()
    for item in sorted(path.iterdir(), key=lambda entry: entry.name.lower()):
        if is_path_ignored(item, ignored_patterns):
            continue

        suffix = "/" if item.is_dir() else ""
        items.append(f"{item.name}{suffix}")

    return items


tool_schema = {
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "Returns a list of files and folders in the specified directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The path to the directory to list. Use '.' for the current directory.",
                },
            },
            "required": ["directory"],
        },
    },
}
