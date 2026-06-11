from pathlib import Path

from workspace import WORKSPACE, save_path


def replace_chunk(path: str, start_line: int, end_line: int, content: str) -> str:
    try:
        if start_line < 1:
            return "Error replacing chunk: start_line must be greater than or equal to 1"

        if end_line < start_line:
            return "Error replacing chunk: end_line must be greater than or equal to start_line"

        file_path = Path(WORKSPACE, save_path(path))

        if not file_path.exists():
            return f"Error replacing chunk: file does not exist: {path}"

        if not file_path.is_file():
            return f"Error replacing chunk: path is not a file: {path}"

        lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)

        if start_line > len(lines):
            return f"Error replacing chunk: start_line is beyond end of file: {path}"

        start_index = start_line - 1
        end_index = min(end_line, len(lines))
        lines[start_index:end_index] = [content]
        file_path.write_text("".join(lines), encoding="utf-8")

        return f"Successfully replaced chunk in file: {path}"
    except Exception as error:
        return f"Error replacing chunk: {error}"


tool_schema = {
    "type": "function",
    "function": {
        "name": "replace_chunk",
        "description": "Replaces an inclusive 1-based line range in a UTF-8 text file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file that should be modified.",
                },
                "start_line": {
                    "type": "integer",
                    "description": "The first 1-based line number to replace.",
                },
                "end_line": {
                    "type": "integer",
                    "description": "The last 1-based line number to replace.",
                },
                "content": {
                    "type": "string",
                    "description": "The UTF-8 text content to insert in place of the removed lines.",
                },
            },
            "required": ["path", "start_line", "end_line", "content"],
        },
    },
}
