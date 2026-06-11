from pathlib import Path


def replace_text(path: str, old_text: str, new_text: str, count: int = 1) -> str:
    try:
        if old_text == "":
            return "Error replacing text: old_text must not be empty"

        file_path = Path(path)

        if not file_path.exists():
            return f"Error replacing text: file does not exist: {path}"

        if not file_path.is_file():
            return f"Error replacing text: path is not a file: {path}"

        content = file_path.read_text(encoding="utf-8")
        occurrences = content.count(old_text)

        if occurrences == 0:
            return f"Error replacing text: text was not found in file: {path}"

        replacement_count = occurrences if count < 0 else min(count, occurrences)
        updated_content = content.replace(old_text, new_text, count)
        file_path.write_text(updated_content, encoding="utf-8")

        return f"Successfully replaced {replacement_count} occurrence(s) in file: {path}"
    except Exception as error:
        return f"Error replacing text: {error}"


tool_schema = {
    "type": "function",
    "function": {
        "name": "replace_text",
        "description": "Replaces UTF-8 text in a file. By default, only the first matching occurrence is replaced.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file that should be modified.",
                },
                "old_text": {
                    "type": "string",
                    "description": "The exact text to replace.",
                },
                "new_text": {
                    "type": "string",
                    "description": "The replacement text.",
                },
                "count": {
                    "type": "integer",
                    "description": "Maximum number of occurrences to replace. Defaults to 1. Use -1 to replace all occurrences.",
                    "default": 1,
                },
            },
            "required": ["path", "old_text", "new_text"],
        },
    },
}
