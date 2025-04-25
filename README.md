# MCP Weather Application (Client-Server)

This project demonstrates a client-server application using the MCP (Model Context Protocol) framework to retrieve weather information.

*   `weather/`: Contains the MCP server code, which fetches data from the National Weather Service (NWS) API.
*   `mcp-client/`: Contains the MCP client code, which interacts with the server and uses LangChain with Groq for natural language queries.

## Description

The **MCP Server** (`weather/`) provides specific tools (`get_alerts`, `get_forecast`) accessible via MCP. It connects to the NWS API to fulfill requests made through these tools.

The **MCP Client** (`mcp-client/`) connects to the MCP server, discovers its tools, and allows users to interact via a chat interface. It uses LangChain and the Groq API (Llama 3 model) to process natural language queries, determine if a server tool is needed, call the tool via MCP if necessary, and formulate a final response.

## Architecture

1.  The **Client** starts and initiates an MCP connection (via stdio) to the **Server** script.
2.  The **Client** discovers the tools available on the **Server**.
3.  The user provides a natural language query to the **Client**.
4.  The **Client** uses the Groq LLM (via LangChain) to interpret the query and potentially identify the need to use a server tool.
5.  If a tool is needed, the **Client** sends an MCP request to the **Server** to execute the specific tool (e.g., `get_forecast`) with the required arguments.
6.  The **Server** executes the tool logic, fetching data from the NWS API.
7.  The **Server** sends the result back to the **Client** via MCP.
8.  The **Client** incorporates the tool's result into the ongoing conversation with the LLM.
9.  The **Client** presents the final LLM-generated response to the user.

## Setup

Detailed setup instructions, including dependency installation and environment configuration (like API keys), can be found in the README files within each component's directory:

*   **Server Setup:** See `weather/README.md`
*   **Client Setup:** See `mcp-client/README.md`

## Running the Application

To run the client and have it automatically start and connect to the server, execute the following command from the **mcp-client/** (the directory containing `client.py`):

```bash
uv run client.py ../weather/weather.py
```