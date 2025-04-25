# MCP Weather Server

This directory contains the server-side code for the MCP Weather Application.

## Description

The MCP Server acts as a backend service. It listens for HTTP requests from clients (like the `mcp-client`), fetches current weather data for a given city from an external weather API (using NWS Api), processes the data, and returns the relevant information to the client, typically in JSON format.

## Technology Stack

*   **Language:** Python
*   **Libraries:** `httpx` (for client configuration), `mcp.server.fastmcp`(for creating FastMCP server instance)
*   **External API:** National Weather Service(NWS) 

## Setup and Installation

### Prerequisites

*   Python 3.x installed.
*   `pip` (Python package installer).

### Steps

1.  **Navigate to the server directory:**
    ```bash
    cd weather/
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python3.12 -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

## Available MCP Tools

This server exposes the following tools that can be called by an MCP client:

1.  **`get_alerts`**
    *   **Description:** Retrieves active weather alerts from the NWS for a specific US state.
    *   **Arguments:**
        *   `state` (str): The two-letter US state code (e.g., "CA", "NY", "TX"). Case-sensitive based on NWS API requirements.
    *   **Returns:** (str) A formatted string containing details of active alerts, separated by `\n---\n`. Returns a specific message if no alerts are found or if there's an error fetching data.

2.  **`get_forecast`**
    *   **Description:** Fetches the weather forecast from the NWS for a specific geographical location defined by latitude and longitude.
    *   **Arguments:**
        *   `latitude` (float): The latitude of the desired location.
        *   `longitude` (float): The longitude of the desired location.
    *   **Returns:** (str) A formatted string containing the weather forecast for the next few periods (up to 5), separated by `\n---\n`. Returns a specific message if forecast data cannot be retrieved.