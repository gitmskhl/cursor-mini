from pathlib import Path

import workspace


def write_chunk(path: str, start_line: int, content: str) -> str:
    try:
        if start_line < 1:
            return "Error writing chunk: start_line must be greater than or equal to 1"

        file_path = Path(workspace.WORKSPACE, workspace.resolve_path(path))
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if file_path.exists() and not file_path.is_file():
            return f"Error writing chunk: path is not a file: {path}"

        if file_path.exists():
            lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)
        else:
            lines = []

        insert_index = min(start_line - 1, len(lines))
        lines[insert_index:insert_index] = [content]
        file_path.write_text("".join(lines), encoding="utf-8")

        return f"Successfully wrote chunk to file: {path}"
    except Exception as error:
        return f"Error writing chunk: {error}"


tool_schema = {
    "type": "function",
    "function": {
        "name": "write_chunk",
        "description": "Inserts UTF-8 text into a file starting at a 1-based line number, creating parent directories automatically.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file that should be modified.",
                },
                "start_line": {
                    "type": "integer",
                    "description": "The 1-based line number where content should be inserted.",
                },
                "content": {
                    "type": "string",
                    "description": "The UTF-8 text content to insert.",
                },
            },
            "required": ["path", "start_line", "content"],
        },
    },
}
