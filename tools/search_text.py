from pathlib import Path

from tools.text_utils import (
    is_binary_file,
    iter_unignored_paths,
    load_pathignore_patterns,
    read_text_file,
)
import workspace


def search_text(directory: str, text: str, encoding: str = "utf-8") -> list[str]:
    workspace_root = Path(workspace.WORKSPACE)
    path = workspace_root / workspace.resolve_path(directory)

    if not path.exists():
        return [f"Directory does not exist: {directory}"]

    if not path.is_dir():
        return [f"Path is not a directory: {directory}"]

    matches: list[str] = []
    ignored_patterns = load_pathignore_patterns(workspace_root)

    for item in iter_unignored_paths(path, ignored_patterns, base_dir=workspace_root):
        if not item.is_file():
            continue

        try:
            if is_binary_file(item, encoding=encoding):
                continue

            if text in read_text_file(item, encoding=encoding):
                matches.append(str(item))
        except Exception:
            continue

    return matches


tool_schema = {
    "type": "function",
    "function": {
        "name": "search_text",
        "description": "Searches text in text files of the specified directory and returns matching files. Binary files are skipped.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The path to the directory where files should be searched.",
                },
                "text": {
                    "type": "string",
                    "description": "The text to search for.",
                },
                "encoding": {
                    "type": "string",
                    "description": "Text file encoding to use while searching. Defaults to utf-8. Examples: utf-8, cp1251, latin-1.",
                    "default": "utf-8",
                },
            },
            "required": ["directory", "text"],
        },
    },
}
