📖 MCP Search Tool with Mistral Summarizer
An interactive command-line search tool that combines SerpAPI web search with Mistral-7B Instruct model summarization. Built using the FastMCP framework for modular tool-based AI systems.



🚀 Features
🔍 Search web queries using SerpAPI
📑 Summarize search results into clean, concise bullet points via Mistral-7B Instruct (Hugging Face Inference API)
📦 Modular client-server design with FastMCP
📄 Environment variable management via .env (Hugging Face & SerpAPI keys)
📡 Async handling for efficient web requests and model calls



📂 Project Structure

search_mcp_project/
├── client/
│   └── gemini_client.py    # MCP client implementation
├── server/
│   └── search_server.py    # MCP server with SerpAPI integration
├── .env                    # API keys (ignored via .gitignore)
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
└── main.py                 # Entry point (if needed)




🛠️ Setup Instructions
1️⃣ Clone the repository

git clone https://github.com/ayushiraj02/MCP_search-tool.git

cd MCP_search-tool


2️⃣ Create a virtual environment
uv venv
source .venv/bin/activate


3️⃣ Install dependencies
uv pip install -r requirements.txt  


4️⃣ Configure environment variables
Create a .env file:
SERPAPI_KEY=your_serpapi_key_here
HF_TOKEN=your_huggingface_token_here


5️⃣ Run the server
uv run server/search_server.py


6️⃣ Run the client

In another terminal tab:
uv run client/gemini_client.py server/search_server.py


📸 Example Usage

💬 Mistral + MCP Client Started!
Type your queries (type 'quit' to exit).

📝 Query: top 10 news
🟢 Response:
• Japan hits record $232 billion M&A deals.
• 21 people killed in Gaza airstrikes.
• China responds to US fentanyl demands.
• France intercepts drones targeting Israel.
• India-US trade talks approaching July 9 deadline.







📚 Tech Stack
🐍 Python 3.10+
🖥️ FastMCP
🌐 SerpAPI
🤖 Hugging Face Inference API (Mistral-7B Instruct)
📦 uv package manager
📄 dotenv for environment management



📌 To-Do / Future Improvements
 Add logging and error handling enhancements
 Support for multiple summarization models
 Dockerize the client-server system
 Add CLI argument parsing for query input


📝 License
This project is licensed under the MIT License.