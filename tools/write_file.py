from pathlib import Path

from workspace import WORKSPACE, save_path


def write_file(path: str, content: str) -> str:
    try:
        file_path = Path(WORKSPACE, save_path(path))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return f"Successfully wrote file: {path}"
    except Exception as error:
        return f"Error writing file: {error}"


tool_schema = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes UTF-8 text content to a file, creating parent directories automatically.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file that should be written.",
                },
                "content": {
                    "type": "string",
                    "description": "The UTF-8 text content to write to the file.",
                },
            },
            "required": ["path", "content"],
        },
    },
}
