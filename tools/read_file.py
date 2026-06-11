from pathlib import Path

from tools.text_utils import is_binary_file


MAX_FILE_SIZE = 100_000


def read_file(
    path: str,
    encoding: str = "utf-8",
    start_line: int = 1,
    end_line: int | None = None,
) -> str:
    try:
        file_path = Path(path)

        if not file_path.exists():
            return f"File does not exist: {path}"

        if not file_path.is_file():
            return f"Path is not a file: {path}"

        if is_binary_file(file_path, encoding=encoding):
            return f"File is binary and cannot be read as text: {path}"

        if start_line < 1:
            return "start_line must be greater than or equal to 1"

        if end_line is not None and end_line < start_line:
            return "end_line must be greater than or equal to start_line"

        selected_lines: list[str] = []
        selected_size = 0
        with file_path.open("r", encoding=encoding) as file:
            for line_number, line in enumerate(file, start=1):
                if line_number < start_line:
                    continue

                if end_line is not None and line_number > end_line:
                    break

                selected_lines.append(line)
                selected_size += len(line.encode(encoding))

                if selected_size > MAX_FILE_SIZE:
                    return "File is too large.\nUse start_line and end_line."

        return "".join(selected_lines)
    except Exception as error:
        return f"Error reading file '{path}': {error}"


tool_schema = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Reads a text file and returns its contents. Binary files are rejected.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the text file that should be read.",
                },
                "encoding": {
                    "type": "string",
                    "description": "Text file encoding to use while reading. Defaults to utf-8. Examples: utf-8, cp1251, latin-1.",
                    "default": "utf-8",
                },
                "start_line": {
                    "type": "integer",
                    "description": "The 1-based line number to start reading from. Defaults to 1.",
                    "default": 1,
                },
                "end_line": {
                    "type": ["integer", "null"],
                    "description": "The 1-based line number to stop reading at. Defaults to null, which reads to the end.",
                },
            },
            "required": ["path"],
        },
    },
}
