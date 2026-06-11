from pathlib import Path


def get_file_info(path: str) -> dict:
    try:
        file_path = Path(path)

        if not file_path.exists():
            return {"error": f"Path does not exist: {path}"}

        is_file = file_path.is_file()
        is_dir = file_path.is_dir()

        return {
            "name": file_path.name,
            "suffix": file_path.suffix,
            "size": file_path.stat().st_size if is_file else 0,
            "is_file": is_file,
            "is_dir": is_dir,
        }
    except Exception as error:
        return {"error": f"Error getting file info for '{path}': {error}"}


tool_schema = {
    "type": "function",
    "function": {
        "name": "get_file_info",
        "description": "Returns basic metadata for a file or directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file or directory to inspect.",
                },
            },
            "required": ["path"],
        },
    },
}
