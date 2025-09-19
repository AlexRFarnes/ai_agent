# get_files_info.py

from pathlib import Path

from google.genai import types


def get_files_info(working_directory: Path, directory: Path | None = None):
    working_path = Path(working_directory).resolve()

    directory_path = working_path

    # If directory is not none then build the target directory path
    if directory:
        directory_path = Path(working_path / directory).resolve()

    # Check if directory is not a directory
    if not directory_path.is_dir():
        return f"Error: {directory} is not a directory"

    # Check if directory is outside of the working directory
    if not directory_path.is_relative_to(working_path):
        return f'Error: Cannot list "{directory}" as it is outside the \
            permitted working directory'

    try:
        files_info = []
        for filename in directory_path.iterdir():
            name = filename.name
            size = filename.stat().st_size
            is_dir = filename.is_dir()
            files_info.append(
                f"- {name}: file_size={size} bytes, \
            is_dir={is_dir}"
            )
        return "\n".join(files_info)

    except (PermissionError, IsADirectoryError) as e:
        return f"Error: {e}"
    except UnicodeDecodeError as e:
        return f"Error: Cannot read file due to encoding issues: {e}"
    except OSError as e:
        return f"Error: Filesystem error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
