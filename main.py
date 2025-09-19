# main.py

import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import call_function
from config import MAX_ITERATIONS
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

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
    for candidate in response.candidates:
        messages.append(candidate.content)

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    messages.append(types.Content(role="user", parts=function_responses))

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    return None


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

    for _ in range(MAX_ITERATIONS):
        try:
            content = generate_content(client, messages, verbose)
            if content:
                print("Final response:")
                print(content)
                break
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print("No response generated after max iterations")


if __name__ == "__main__":
    main()
