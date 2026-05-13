import os
import asyncio
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp.client.stdio import StdioServerParameters

from google.adk.runners import InMemoryRunner
from google.genai import types

# 1. Load your Gemini API Key from the .env file in the root directory
root_dir = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(root_dir, '.env'))

# 2. Define the connection to the MCP Server (The Hands)
mcp_connection = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[os.path.join(os.path.dirname(__file__), "mcp_server.py")]
        )
    )
)

# 3. Define the AI Brain (The Agent)
email_agent = Agent(
    name="executive_assistant",
    model="gemini-flash-latest", 
    description="An executive assistant that manages your Gmail inbox.",
    instruction="""You are a professional email assistant. 
    You have access to tools to read the user's recent emails and send new ones. 
    Always summarise incoming emails clearly. If asked to send an email, draft it and confirm the details first.""",
    tools=[mcp_connection]
)

# 4. Create the Runner to manage the agent
runner = InMemoryRunner(agent=email_agent, app_name="email_assistant")

# 5. The Terminal Chat Interface
async def main():
    await runner.session_service.create_session(
        app_name="email_assistant",
        user_id="local_user",
        session_id="session_1"
    )

    print("🤖 The Email Agent is online! (Type 'quit' to exit)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            print("Shutting down the programme...")
            break
        
        print("\nAgent: ", end="", flush=True)
        
        message_content = types.Content(role='user', parts=[types.Part(text=user_input)])
        
        # FIX: Wrap the execution in a robust try...except block to handle API rate limits gracefully
        try:
            async for event in runner.run_async(
                user_id="local_user",
                session_id="session_1",
                new_message=message_content
            ):
                if hasattr(event, 'is_final_response') and event.is_final_response():
                    print(event.content.parts[0].text, end="", flush=True)
                    
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print("\n[System Notice] We have hit the Google API rate limit. Please wait about 15 seconds and try asking again.", end="")
            else:
                print(f"\n[System Error] An unexpected error occurred: {error_msg}", end="")
                
        print("\n")

if __name__ == "__main__":
    asyncio.run(main())