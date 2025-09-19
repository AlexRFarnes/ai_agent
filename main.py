# main.py

import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

load_dotenv()

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions]
        ),
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        for function_call_part in response.function_calls:
            name = function_call_part.name
            args = dict(function_call_part.args or {})
            if name == "run_python_file":
                args["args"] = args.get("args") or []
            function_call_result = call_function(function_call_part, verbose)
            if not function_call_result.parts[0].function_response.response:
                raise Exception(f"Something went wrong while calling function: {name}")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print("Response:", response.text)


def call_function(
    function_call_part: types.FunctionCallPart, verbose: bool = False
) -> types.Content:
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    working_directory = "./calculator"
    function_name = function_call_part.name
    args = dict(function_call_part.args or {})
    function_map = {
        "run_python_file": run_python_file,
        "write_file": write_file,
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
    }

    function = function_map.get(function_name)

    if not function:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args["working_directory"] = working_directory
    function_result = function(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print('Usage: python main.py "your prompt goes here" [--verbose]')
        print('Example: python main.py "How to build a to-do app?"')
        sys.exit(1)

    prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {prompt}")

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    generate_content(client, messages, verbose)


if __name__ == "__main__":
    main()
