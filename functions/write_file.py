# write_file.py


from pathlib import Path

from google.genai import types


def write_file(working_directory: Path, file_path: Path, content: str):
    working_path = Path(working_directory).resolve()
    file_path = Path(working_path / file_path).resolve()

    if not file_path.is_relative_to(working_path):
        return f'Error: Cannot write to "{file_path.name}" as it is outside \
            the permitted working directory'

    try:
        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        # Create the file if it doesn't exist
        with open(file_path, mode="w", encoding="utf-8") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path.name}" \
                ({len(content)} characters written)'

    except (PermissionError, IsADirectoryError) as e:
        return f"Error: {e}"
    except UnicodeEncodeError as e:
        return f"Error: Cannot write file due to encoding issues: {e}"
    except OSError as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)
