# AI Coding Agent

A modular, containerized AI coding agent built with **FastAPI** and **LangGraph**, powered by **Google's Gemini models**. The agent autonomously handles file system operations within a secure workspace using an agentic loop architecture.

---

## Architecture Overview

The system follows a clean separation of concerns:

```
User Request -> FastAPI (/chat) -> LangGraph Workflow -> Gemini Model -> Tool Execution -> Response
```

| Layer | File(s) | Responsibility |
|---|---|---|
| **API** | `main.py` | Exposes `/chat` endpoint via FastAPI |
| **Agent Logic** | `graph/workflow.py` | Stateful LangGraph workflow with tool-call feedback loop |
| **Configuration** | `core/config.py` | Loads environment variables via `python-dotenv` |
| **Model** | `core/model.py` | Initializes `gemini-2.5-flash` and binds tools |
| **System Prompt** | `core/prompt.py` | Defines agent identity and behavior instructions |
| **State** | `core/state.py` | `TypedDict` schema for LangGraph state management |
| **Tools** | `tools/file_tools.py` | `create_file` and `read_file` for workspace operations |

---

## Project Structure

```
ai-coding-agent/
├── core/
│   ├── config.py           # Environment and API key management
│   ├── model.py            # Gemini model initialization & tool binding
│   ├── prompt.py           # System instructions for the AI agent
│   └── state.py            # TypedDict for LangGraph state
├── graph/
│   └── workflow.py         # LangGraph workflow definition
├── tools/
│   └── file_tools.py       # File system manipulation tools
├── workspace/              # Default directory for agent-created files
├── main.py                 # FastAPI entry point
├── Dockerfile              # Container build instructions
├── docker-compose.yml      # Multi-container orchestration
└── requirements.txt        # Python dependencies
```

---

## Tech Stack

- **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Agent Orchestration:** [LangGraph](https://langchain-ai.github.io/langgraph/)
- **AI Model:** [Google Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/) via LangChain Google GenAI
- **Containerization:** Docker & Docker Compose
- **Environment Management:** python-dotenv

---

## Getting Started

### Prerequisites

- Docker & Docker Compose installed, **or** Python 3.10+
- A valid [Google AI API key](https://aistudio.google.com/app/apikey)

### 1. Configure Environment

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Then open `.env` and set your API key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

---

### Option A -- Docker (Recommended)

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

---

### Option B -- Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## API Usage

### `POST /chat`

Send a natural language instruction to the agent.

**Request:**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a Python script called hello.py that prints Hello World"}'
```

**Payload Schema:**

```json
{
  "message": "string"
}
```

**Response:**

The agent will autonomously decide which tools to use, execute them, and return a confirmation message. Generated files are saved to the `workspace/` directory.

**Example Response:**

```json
{
  "response": "I've created hello.py in the workspace directory. The script contains a single print statement that outputs 'Hello World' when executed."
}
```

---

## How the Agent Works

1. **User sends a message** to `POST /chat`
2. **FastAPI** passes the message into the **LangGraph workflow**
3. The **Gemini model** processes the message and decides whether to call a tool
4. If a tool is needed (e.g., `create_file`), the **tool node** executes it within `workspace/`
5. The result is fed back to the model, which produces a **final natural language response**
6. The response is returned to the user

This feedback loop continues until the model determines no further tool calls are necessary.

---

## Available Tools

| Tool | Description |
|---|---|
| `create_file` | Creates or overwrites a file in the `workspace/` directory |
| `read_file` | Reads and returns the contents of a file from `workspace/` |

---

## Security Notes

- All file operations are sandboxed to the `workspace/` directory
- The `GOOGLE_API_KEY` is loaded from `.env` and never hardcoded
- Docker provides additional isolation between the agent and the host system


## Author

**Abdullah Aarif Shaikh** -- [GitHub](https://github.com/abdullahaarifshaikh/ai-coding-agent)