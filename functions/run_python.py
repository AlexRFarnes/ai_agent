# run_python_file.py

import subprocess
import sys
from pathlib import Path

from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    working_path = Path(working_directory).resolve()
    file = Path(working_path / file_path).resolve()

    if not file.is_relative_to(working_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not file.exists():
        return f'Error: File "{file_path}" not found.'

    if file.suffix != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            [sys.executable, file, *args],
            check=True,
            timeout=30,
            capture_output=True,
            text=True,
        )
        stdout = f"STDOUT:{completed_process.stdout.strip()}"
        stderr = f"STDERR:{completed_process.stderr.strip()}"
        returncode = (
            f"Process exited with code {completed_process.returncode}"
            if completed_process.returncode
            else "0"
        )
        if not stdout and not stderr:
            result = f"{returncode}\nNo output produced."
        else:
            result = f"{stdout}\n{stderr}\n{returncode}"
        return result

    except subprocess.TimeoutExpired as e:
        return f"Error: executing Python file: {e}"
    except subprocess.CalledProcessError as e:
        return f"Error: executing Python file: {e}"
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified Python file, constrained to the working directory.",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                default=[],
                description="Optional.The arguments to pass to the Python file. If not provided, the Python file will be run without any arguments.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="The argument to pass to the Python file.",
                ),
            ),
        },
    ),
)
