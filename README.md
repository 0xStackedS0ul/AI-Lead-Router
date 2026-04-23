# AI Lead Router: Intelligent Webhook Processing

An event-driven Python microservice that acts as an intelligent webhook listener. It intercepts incoming lead data, uses an LLM (Gemini/OpenAI) to extract structured JSON (intent, budget, urgency), and routes the data to a local SQLite database with priority tagging.

# // Core Features

[WEBHOOK] Event Listener: FastAPI-based endpoint that continuously listens for incoming POST requests from external sources (e.g., Typeform, Make, n8n).

[AI PARSER] Structured Extraction: Implements LLM logic to convert unstructured natural language into strictly formatted JSON, bypassing hallucination risks.

[ROUTER] Decision Engine: Evaluates the qualified JSON payload against business logic to assign priority flags (e.g., URGENT_ALERT_REQUIRED).

[STORAGE] Persistence: Automatically initializes and writes verified lead records into a local SQLite database.

# // Project Architecture

```text
* ai-lead-router/
* ├── core/                  # Core business logic (Separation of Concerns)
* │   ├── __init__.py
* │   ├── ai_parser.py       # Level 1: LLM orchestration and JSON enforcement
* │   └── routing.py         # Level 2: Database connection and routing logic
* ├── data/                  # Local database storage (Git-ignored)
* │   └── leads.db         
* ├── .env.example           # Template for environment variables
* ├── .gitignore             # Ignored files and sensitive data
* ├── requirements.txt       # Python dependencies
* ├── main.py                # Level 0: FastAPI Server & Orchestrator
* ├── test_webhook.py        # Client simulation script
* └── README.md              # Project documentation

// Installation & Setup
[1] Clone the repository
git clone https://github.com/yourusername/ai-lead-router.git
cd ai-lead-router

[2] Install dependencies
It is recommended to use a virtual environment (e.g., venv)
pip install -r requirements.txt

[3] Configure Environment Variables
Create a .env file in the root directory and add your API credentials:
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here

[4] Run the Pipeline
Execute the FastAPI server:
python main.py

In a separate terminal, trigger the test webhook:
python test_webhook.py

// Future Improvements & Roadmap
[TODO: NOTIFICATIONS] Connect the routing engine to a Telegram/Slack bot for real-time alerts on high-priority leads.
[TODO: AUTHENTICATION] Add an API key dependency to the FastAPI /webhook route to prevent unauthorized data injection.