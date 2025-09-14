# get_file_content.py

from pathlib import Path

MAX_CHARS = 10_000


def get_file_content(working_directory, file_path):
    working_path = Path(working_directory).resolve()
    file = Path(working_path / file_path).resolve()

    if not file.is_relative_to(working_path):
        return f'Error: Cannot read "{file.name}" as it is outside the \
            permitted working directory'

    if not file.is_file():
        return f'Error: File not found or is not a regular file: \
        "{file.name}"'

    try:
        with file.open(encoding="utf-8") as f:
            result = f.read(MAX_CHARS)
            if file.stat().st_size > MAX_CHARS:
                result += f'[...File "{file.name}" truncated at \
                        {MAX_CHARS} characters]'

            return result
    except (PermissionError, IsADirectoryError) as e:
        return f"Error: {e}"
    except UnicodeDecodeError as e:
        return f"Error: Cannot read file due to encoding issues: {e}"
    except OSError as e:
        return f"Error: Filesystem error: {e}"
