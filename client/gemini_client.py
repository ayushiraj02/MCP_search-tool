# uv run client/gemini_client.py server/search_server.py


import asyncio
import sys
import os
from contextlib import AsyncExitStack
from typing import Optional
from dotenv import load_dotenv
import google.generativeai as genai

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

import requests

HUGGINGFACE_API_TOKEN = os.getenv("HF_TOKEN")  
print("Hugging Face API Token:", HUGGINGFACE_API_TOKEN)
# store in .env

# def call_huggingface(prompt: str, model="facebook/bart-large-cnn"):
#     try:
#         headers = {
#             "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
#         }
#         json_data = {
#             "inputs": prompt,
#             "parameters": {"max_new_tokens": 300}
#         }

#         response = requests.post(
#             f"https://api-inference.huggingface.co/models/{model}",
#             headers=headers,
#             json=json_data
#         )

#         print("👉 Status Code:", response.status_code)
#         print("👉 Raw Response:", response.text)    
#         result = response.json()

#         return result[0]['generated_text']

#     except Exception as e:
#         print(f"❌ Error calling Hugging Face API: {str(e)}")
#         return "Sorry, couldn't process your request."


def call_mistral_model(prompt: str):
    try:
        client = InferenceClient(
            provider="featherless-ai",
            api_key=os.getenv("HF_TOKEN"),
        )

        completion = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[{"role": "user", "content": prompt}]
        )

        return completion.choices[0].message.content

    except Exception as e:
        print(f"❌ Mistral Error: {str(e)}")
        return "Sorry, couldn't process your request."


class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server"""
        is_python = server_script_path.endswith('.py')
        if not is_python:
            raise ValueError("Server script must be a .py file")

        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path]
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()

        response = await self.session.list_tools()
        print("\n✅ Connected to server with tools:", [tool.name for tool in response.tools])



    async def process_query(self, query: str) -> str:
        """Always search via SerpAPI and summarize with Mistral."""
        result = await self.session.call_tool("search_web", {"query": query})
        print(f"\n🟢 MCP Search Result:\n{result}")

        if not result.content or result.content[0].text.strip() == "Error fetching search results:":
            return "❌ Couldn't fetch search results. Please try a different query."

        summary_prompt = (
            f"You are a helpful AI assistant.\n\n"
            f"Given the following search results about **{query}**:\n\n{result.content}\n\n"
            f"Summarize the top 5 key points in clean, concise bullet points. Avoid URLs and filler text."
        )

        return call_mistral_model(summary_prompt)


 
    
    async def chat_loop(self):
        """Interactive chat"""
        print("\n💬 Mistral + MCP Client Started!")

        print("Type your queries (type 'quit' to exit).")

        while True:
            try:
                query = input("\n📝 Query: ").strip()
                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n🟢 Response:\n" + response)

            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python gemini_client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
