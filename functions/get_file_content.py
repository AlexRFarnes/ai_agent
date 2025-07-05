# get_file_content.py

from pathlib import Path

MAX_CHARS = 10_000


def get_file_content(working_directory, file_path):
    working_path = Path(working_directory).resolve()
    file_path = (working_path / file_path).resolve()

    if not file_path.is_relative_to(working_path):
        return f'Error: Cannot read "{file_path.name}" as it is outside the permitted working directory'

    if not file_path.is_file():
        return f'Error: File not found or is not a regular file: "{file_path.name}"'

    try:
        with file_path.open() as file:
            result = file.read(MAX_CHARS)
            if file_path.stat().st_size > MAX_CHARS:
                result += (
                    f'[...File "{file_path.name}" truncated at {MAX_CHARS} characters]'
                )

            return result
    except Exception as e:
        return f"Error: {e}"
