import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print("Response:", response.text)


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
