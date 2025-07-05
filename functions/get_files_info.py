# get_files_info.py

from pathlib import Path


def get_files_info(working_directory, directory=None):
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
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    try:
        files_info = []
        for filename in directory_path.iterdir():
            name = filename.name
            size = filename.stat().st_size
            is_dir = filename.is_dir()
            files_info.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(files_info)

    except Exception as e:
        return f"Error: {e}"
