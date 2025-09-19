# AI Agent in Python

> ⚠️ **WARNING: FOR EDUCATIONAL PURPOSES ONLY** ⚠️
>
> This is a learning project. Unlike professional AI coding assistants like Cursor's agent mode, this implementation lacks critical safety features, error handling, and security measures. It is designed solely for educational purposes to understand how AI agents work under the hood.

A toy agentic code editor built in Python, similar to Claude Code or Cursor's agent mode. This project demonstrates how to create an LLM-powered command-line program capable of reading, updating, and running Python code using the Gemini API.

## About This Project

This project was completed as part of the [Boot.dev Backend Developer Path](https://www.boot.dev) course ["Build an AI Agent in Python"](https://www.boot.dev/courses/build-ai-agent-python). The course teaches how LLMs and agentic coding tools work by building a real AI agent from scratch.

### Course Overview

- **Duration**: 12 hours of content across 18 lessons
- **Focus**: Understanding how agents work using the free Google Gemini API
- **Skills Learned**: Function calling, feedback loops, and building agentic tools
- **Final Project**: An agent that can find and fix bugs in real projects

## Features

The AI Agent can perform the following operations:

- **List files and directories** - Explore the project structure
- **Read file contents** - Analyze existing code
- **Execute Python files** - Run code with optional arguments
- **Write or overwrite files** - Modify and create files

## Architecture

The agent uses a feedback loop system with the following components:

- **Main Agent Loop** (`main.py`) - Orchestrates the conversation and function calling
- **Function Calling System** (`call_function.py`) - Handles function execution based on AI decisions
- **Available Functions** (`functions/`) - Core capabilities for file operations and code execution
  - `get_files_info.py` - List files and directories
  - `get_file_content.py` - Read file contents
  - `run_python.py` - Execute Python files
  - `write_file.py` - Create and modify files
- **Configuration** (`config.py`) - Settings for the agent behavior

## Prerequisites

- Python 3.12+
- Google Gemini API key
- `uv` package manager (recommended) or pip

## Setup

1. Clone this repository
2. Install dependencies:

   ```bash
   uv sync
   # or
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

Run the AI agent with a prompt:

```bash
python main.py "your prompt goes here" [--verbose]
```

### Examples

```bash
# Basic usage
python main.py "How to build a to-do app?"

# With verbose output to see function calls
python main.py "List all files in the project" --verbose

# Ask the agent to fix a bug
python main.py "Find and fix any bugs in the calculator module" --verbose
```

The agent will:

1. Understand your request
2. Plan a series of function calls
3. Execute the plan step by step
4. Provide a final response with results

## Project Structure

```
ai_agent/
├── main.py              # Main agent loop and orchestration
├── call_function.py     # Function calling handler
├── config.py           # Configuration settings
├── functions/          # Available agent functions
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python.py
│   └── write_file.py
├── calculator/         # Example target project for testing
├── tests.py           # Test cases
├── pyproject.toml     # Project dependencies
└── README.md          # This file
```

## Key Learning Outcomes

From the [Boot.dev course "Build an AI Agent in Python"](https://www.boot.dev/courses/build-ai-agent-python):

1. **Understanding LLMs** - How to send prompts to the Gemini API using the Python client library
2. **Function Calling** - Writing functions your AI agent needs to modify files and run Python code
3. **Agent Architecture** - Giving your AI agent the ability to call functions based on system prompts and context
4. **Feedback Loops** - Making the tool truly "agentic" with proper feedback mechanisms

## Technology Stack

- **Language**: Python 3.12+
- **LLM API**: Google Gemini 2.0 Flash
- **Function Calling**: Google Genai Python client
- **Environment Management**: python-dotenv
- **Package Management**: uv

## License

This project was created as part of the Boot.dev educational curriculum. See the [Boot.dev course](https://www.boot.dev/courses/build-ai-agent-python) for more information about the learning objectives and curriculum.

---

_Built as part of the [Boot.dev Backend Developer Path](https://www.boot.dev/) - Learn modern backend development skills through hands-on projects._
