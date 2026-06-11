from pathlib import Path
import subprocess

import workspace


def execute_bash(path: str, timeout: int = 5) -> dict:
    try:
        file_path = Path(workspace.WORKSPACE, workspace.resolve_path(path))

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
            ["bash", str(file_path)],
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
            "stderr": f"Bash execution timed out after {timeout} seconds",
        }
    except Exception as error:
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": f"Error executing Bash file: {error}",
        }


tool_schema = {
    "type": "function",
    "function": {
        "name": "execute_bash",
        "description": "Executes a Bash script and returns its process result.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the Bash script to execute.",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Maximum execution time in seconds. Defaults to 5.",
                    "default": 5,
                },
            },
            "required": ["path"],
        },
    },
}
