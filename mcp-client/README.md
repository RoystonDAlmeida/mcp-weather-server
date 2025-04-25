# MCP Client with LangChain and Groq Integration

This directory contains an advanced MCP client that integrates with LangChain and the Groq API to provide an interactive chat experience enhanced by tools available from a connected MCP server.

## Description

This client connects to a specified MCP server (running locally via stdio) and discovers the tools it offers. It then uses a Large Language Model (LLM) hosted on Groq (specifically Llama 3 70b) to understand user queries. If the LLM determines that a query requires information or actions available through the MCP server's tools, the client executes the appropriate tool via the MCP connection and incorporates the result back into the conversation with the LLM before presenting the final response to the user.

## Features

*   Connects to any MCP server script (`.py` or `.js`) using stdio transport.
*   Dynamically lists and utilizes tools provided by the connected MCP server.
*   Integrates with LangChain for managing the conversation flow.
*   Uses the fast Groq API for LLM inference (Llama 3 70b model).
*   Handles LLM-driven tool selection and execution.
*   Provides an interactive command-line chat interface.
*   Loads API keys securely from a `.env` file.

## Technology Stack

*   **Language:** Python
*   **Core Libraries:**
    *   `mcp-lib`: For MCP client session management and stdio communication.
    *   `langchain-groq`: For interacting with the Groq LLM API via LangChain.
    *   `langchain-core`: Core abstractions for LangChain messages and tools.
    *   `python-dotenv`: For loading environment variables (like API keys) from a `.env` file.
    *   `asyncio`: For handling asynchronous operations.

## Setup and Installation

### Prerequisites

*   Python 3.x installed (Python 3.12+ recommended).
*   `uv` installed (an extremely fast Python package installer and resolver). Install via pip: `pip install uv`.
*   A Groq API Key. You can get one from GroqCloud.
*   An MCP server script (like the one in the `../weather/` directory) ready to be run.

### Steps

1.  **Navigate to the client directory:**
    ```bash
    # Assuming you are in the project root
    cd mcp-client/
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python3.12 -m venv venv
    # Activate the environment
    # On Linux/macOS:
    source .venv/bin/activate
    # On Windows PowerShell:
    # .\venv\Scripts\Activate.ps1
    # On Windows Command Prompt:
    # .\venv\Scripts\activate.bat
    ```
3.  **Install dependencies using uv:**
    ```bash
    uv pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**
    In the `mcp-client/` directory, create a file named `.env` and add your Groq API key:
    ```dotenv
    GROQ_API_KEY = "your_groq_api_key_here"
    ```