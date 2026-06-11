from pathlib import Path
import subprocess
import sys


def execute_python(path: str, timeout: int = 5, args: list[str] | None = None) -> dict:
    try:
        file_path = Path(path)

        if not file_path.exists():
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": f"File does not exist: {path}",
            }

        if not file_path.is_file():
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": f"Path is not a file: {path}",
            }

        result = subprocess.run(
            [sys.executable, str(file_path), *(args or [])],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
        )

        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired as error:
        return {
            "success": False,
            "returncode": -1,
            "stdout": error.stdout or "",
            "stderr": f"Python execution timed out after {timeout} seconds",
        }
    except Exception as error:
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": f"Error executing Python file: {error}",
        }


tool_schema = {
    "type": "function",
    "function": {
        "name": "execute_python",
        "description": "Executes a Python file and returns its process result.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the Python file to execute.",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Maximum execution time in seconds. Defaults to 5.",
                    "default": 5,
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Command-line arguments to pass to the Python file. Defaults to an empty list.",
                    "default": [],
                },
            },
            "required": ["path"],
        },
    },
}
