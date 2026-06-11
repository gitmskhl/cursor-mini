from pathlib import Path

from workspace import WORKSPACE, save_path


def append_file(path: str, content: str) -> str:
    try:
        file_path = Path(WORKSPACE, save_path(path))
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("a", encoding="utf-8") as file:
            file.write(content)

        return f"Successfully appended to file: {path}"
    except Exception as error:
        return f"Error appending file: {error}"


tool_schema = {
    "type": "function",
    "function": {
        "name": "append_file",
        "description": "Appends UTF-8 text content to a file, creating parent directories automatically.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file that should be appended.",
                },
                "content": {
                    "type": "string",
                    "description": "The UTF-8 text content to append to the file.",
                },
            },
            "required": ["path", "content"],
        },
    },
}
