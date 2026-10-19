Tool Calling AI Assistant

A local Ai Assistant that can use tools to answer questions. It runs on your own machine using OLLama + Llama 3.1.
Ask it to calculate something or check wheather - it will pick the right tool and do it.

"E.g.," 'Calculate 15% of 2000' or 'What is the weather of Jammu?'
<img width="1917" height="1007" alt="Screenshot 2026-10-20 042726" src="https://github.com/user-attachments/assets/7162131b-2e8c-469c-a503-0e7bdf951935" />


#features
LLM decide when to use a tool
% calculator tool
Weather tool using Open_Meteo API
Input validation with Pydantic
FastApi backend +Simple HTML/CSS?JS frontend
Runs locacly, no API key needed
<img width="1917" height="1078" alt="Screenshot 2026-10-20 042700" src="https://github.com/user-attachments/assets/f7ab7f34-a3a1-49a7-8519-bdad07e38eba" />

### How it Works
User -> Chat UI -> FastAPI (/chat) -> Ollama (Llama 3.1) -> Selects Tool -> Python Function -> LLM generates final answer
### Tech Stack
Python, Ollama, Llama 3.1, FastAPI, Pydantic, HTTPX, HTML/CSS/JS
### Architecture
User
  |
  v
Web Chat Interface
HTML + CSS + JavaScript
  |
  v
FastAPI Backend
POST /chat
  |
  v
AI Agent
Ollama + Llama 3.1
  |
  v
Tool Selection
  |
  +---------------------+
  |                     |
  v                     v
Percentage Calculator   Weather Tool
Python + Pydantic       Open-Meteo API
  |                     |
  +----------+----------+
             |
             v
      Tool Result
             |
             v
       LLM Response
             |
             v
      Chat Interface


<img width="1916" height="982" alt="Screenshot 2026-10-20 042917" src="https://github.com/user-attachments/assets/73f37ed6-0c73-47be-be24-4178fb111569" />


### Technology

Purpose

Python

Core application and tool implementation

Ollama

Local LLM inference

Llama 3.1

Language model used by the agent

FastAPI

Backend REST API

Pydantic

Input validation and data schemas

HTTPX

HTTP requests to the weather API

HTML

Web interface structure

CSS

UI styling and responsive layout

JavaScript

Chat interactions and API communication

Pytest

Automated testing

Open-Meteo API

Weather data retrieval

Git & GitHub

Version control and project hosting

📁 Project Structure

Tool-Calling-AI-Assistant/
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── main.py
│   ├── schemas.py
│   └── tools.py
├── tests/
│   └── test_tools.py
├── index.html
├── style.css
├── script.js
├── requirements.txt
├── .gitignore
└── README.md



💻 Getting Started

Prerequisites

Install the following before running the project:

Python 3.10 or a compatible version

Git

Ollama

A local Ollama model

1. Clone the repository

git clone https://github.com/YOUR-USERNAME/Tool-Calling-AI-Assistant.git
cd Tool-Calling-AI-Assistant

Replace YOUR-USERNAME with your GitHub username.

2. Create and activate a virtual environment

Windows PowerShell

python -m venv venv
.\venv\Scripts\Activate.ps1

3. Install dependencies

python -m pip install -r requirements.txt

4. Download the model

ollama pull llama3.1

5. Start the backend

python -m uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000

Explore the interactive API documentation at:

http://127.0.0.1:8000/docs

6. Start the frontend

Open index.html using the VS Code Live Server extension.

Keep the backend and Ollama running while using the application. If your browser blocks frontend requests, configure CORS in app/main.py for your actual frontend origin.

🔌 API Reference

GET /

Checks whether the backend is running.

POST /chat

Accepts a user question and returns the assistant's response.

Example request

{
  "question": "Calculate 15% of 2000"
}

Example response

{
  "question": "Calculate 15% of 2000",
  "answer": "15% of 2000 is 300."
}

The exact wording of the answer may vary depending on the model's response.

🧪 Testing

Run the automated tests with:

python -m pytest -v

The tests cover tool behavior and selected error scenarios. Expand the test suite as additional functionality is added.

🔒 Validation and Error Handling

Calculator inputs are validated using Pydantic.

Percentage values must be between 0 and 100.

Negative amounts are rejected.

Weather lookup handles missing cities and HTTP or parsing failures.

The agent has a maximum execution-step limit.

Logging helps identify tool-selection and LLM connection problems.

🎯 Learning Objectives

This project explores practical concepts used in AI engineering:

LLM tool calling and function schemas

AI agent execution loops

Connecting LLMs with Python functions

REST API development with FastAPI

Structured input validation using Pydantic

Integrating external APIs

Local LLM inference using Ollama

Error handling, logging, and automated testing

Connecting a JavaScript frontend to a Python backend

🗺️ Future Improvements

Display tool calls and their results in the UI.

Add conversation history and a new-chat option.

Expand the automated test suite.

Improve tool-call validation and failure recovery.

Add more tools, such as unit conversion, search, and document retrieval.

Add structured agent traces and execution monitoring.

Deploy the frontend and backend with an inference setup that works independently of the developer's laptop.

👩‍💻 Author

Samridhi Sharma

AI Automation Engineer | Python | GenAI | LLM Applications

GitHub: @shokinw

LinkedIn: Samridhi Sharma

Built as a hands-on project to explore how LLMs can use tools to perform useful tasks beyond text generation.
