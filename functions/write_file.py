# write_file.py

from pathlib import Path


def write_file(working_directory, file_path, content):
    working_path = Path(working_directory).resolve()
    file_path = Path(working_path / file_path).resolve()

    if not file_path.is_relative_to(working_path):
        return f'Error: Cannot write to "{file_path.name}" as it is outside the permitted working directory'

    try:
        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        # Create the file if it doesn't exist
        with file_path.open(mode="w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path.name}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
