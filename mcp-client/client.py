import asyncio
from typing import Optional, Dict, List, Any
from contextlib import AsyncExitStack
import sys
import os
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# ChatGroq packages
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

load_dotenv()  # load environment variables from .env

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.llm = ChatGroq(
            api_key = os.getenv("GROQ_API_KEY"),
            model = "llama3-70b-8192"
        )

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server
        
        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")
            
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        await self.session.initialize()
        
        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using ChatGroq with manually defined tools"""
        
        # Get available tools from the MCP server
        response = await self.session.list_tools()
        
        # Create simple tool definitions as dictionaries
        tool_defs = []
        for tool in response.tools:
            # Convert MCP tool to LangChain tool definition format
            parameters = {}
            if hasattr(tool, "inputSchema") and tool.inputSchema:
                # If there's a schema, add it (simplified)
                parameters = {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
                # You could add more schema details here if needed
            
            tool_defs.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": parameters
                }
            })
            
        # LangChain message history
        messages = [HumanMessage(content=query)]
        
        # Initial LLM call with tool definitions
        llm_response = await self.llm.ainvoke(
            messages,
            tools=tool_defs
        )

        final_text = []
        
        # Check if the response has tool calls
        if not hasattr(llm_response, 'tool_calls') or not llm_response.tool_calls:
            return llm_response.content
        
        # Handle tool calls
        for tool_call in llm_response.tool_calls:
            try:
                # Execute tool through MCP
                result = await self.session.call_tool(
                    tool_call['name'],
                    tool_call['args']
                )
                
                # Extract the string content from TextContent object
                if hasattr(result.content, 'text'):
                    tool_result_content = result.content.text
                else:
                    tool_result_content = str(result.content)

                tool_result = f"[Tool {tool_call['name']} result: {tool_result_content}]"
                final_text.append(tool_result)
                
                # Add tool result to conversation
                messages.append(AIMessage(
                    content="",
                    tool_calls=[tool_call]
                ))
                messages.append(ToolMessage(
                    content=tool_result_content,
                    tool_call_id=tool_call['id']
                ))
                
                # Get follow-up response
                follow_up = await self.llm.ainvoke(messages)
                final_text.append(follow_up.content)
            except Exception as e:
                final_text.append(f"Error executing tool {tool_call['name']}: {str(e)}")

        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                
                if query.lower() == 'quit':
                    break
                    
                response = await self.process_query(query)
                print("\n" + response)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)
        
    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
