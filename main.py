import os
import sys

from dotenv import load_dotenv
from google import genai

load_dotenv()


def main():
    args = sys.argv[1:]

    if not args:
        print('Usage: python main.py "your prompt goes here"')
        print('Example: python main.py "How to build a to-do app?"')
        sys.exit(1)

    prompt = " ".join(args)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt,
    )

    print(
        f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}"
    )
    print(response.text)


if __name__ == "__main__":
    main()
