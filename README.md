# 🧠 Research Intelligence Agent
### Multi-Agent Research Intelligence System | Agents League Hackathon 2026

[![Track](https://img.shields.io/badge/Track-Reasoning%20Agents-blue)](.)
[![IQ Layer](https://img.shields.io/badge/Microsoft%20IQ-Foundry%20IQ-purple)](.)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green)](.)
[![Azure](https://img.shields.io/badge/Azure-AI%20Foundry-0078D4)](.)

---

## 🎯 Problem Statement

Information on the web is fragmented, contradictory, and difficult to trust.
Researchers, students, and professionals spend hours manually searching, reading,
cross-referencing, and synthesising sources — only to still be uncertain about what to believe.

**Research Intelligence Agent** solves this by deploying a team of 5 specialised AI agents
that autonomously search, read, fact-check, and synthesise information into a structured,
confidence-scored research report — in seconds.

---

## 🏗️ Architecture

```
User (Browser)
     │
     ▼
React Frontend  ──────────────────  Azure Static Web Apps (free tier)
     │ HTTP/REST
     ▼
FastAPI Backend  ─────────────────  Azure App Service
     │
     ▼
┌─────────────────────────────────────────┐
│       ORCHESTRATOR AGENT                │ ◄── Foundry IQ (Microsoft IQ Layer)
└──────┬──────────┬──────────┬────────────┘
       ▼          ▼          ▼
  Search      Reader     Fact-Check
  Agent       Agent        Agent
       └──────────┴──────────┘
                  ▼
           Synthesis Agent
                  ▼
     Confidence-Scored Research Report
```

### Agent Roles

| Agent | Responsibility |
|---|---|
| **Orchestrator** | Coordinates pipeline, manages agent handoffs via Foundry IQ |
| **Search Agent** | Uses Grounding with Bing Search to find sources |
| **Reader Agent** | Fetches and extracts key facts from web pages |
| **Fact-Check Agent** | Cross-references sources, detects contradictions |
| **Synthesis Agent** | Produces final report with confidence-scored findings |

---

## 💡 Microsoft Technologies Used

| Technology | Role |
|---|---|
| **Azure AI Foundry** | Powers all 5 agents via Foundry IQ intelligence layer |
| **Grounding with Bing Search** | Real-time web search for the Search Agent |
| **Azure App Service** | Hosts the FastAPI Python backend |
| **Azure Static Web Apps** | Hosts the React frontend |
| **Azure Managed Identity** | Passwordless authentication (DefaultAzureCredential) |
| **Azure Developer CLI (azd)** | One-command deployment to Azure |

---

## 🚀 Local Setup — Step by Step

### Prerequisites
- Python 3.10+
- Node.js 18+
- Azure account (free at portal.azure.com)
- Azure CLI installed and logged in (`az login`)
- Azure AI Foundry project created with:
  - gpt-4o model deployed
  - Grounding with Bing Search resource connected

### Step 1 — Unzip and enter folder
```bash
unzip research-intelligence-agent.zip
cd research-intelligence-agent
```

### Step 2 — Python virtual environment
```bash
# Mac/Linux
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### Step 3 — Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Install frontend dependencies
```bash
cd frontend
npm install
cd ..
```

### Step 5 — Configure credentials
```bash
cp .env.example .env
# Open .env in a text editor and fill in your values
```

Your `.env` must contain:
```env
AZURE_AI_FOUNDRY_PROJECT_ENDPOINT=https://YOUR-RESOURCE.services.ai.azure.com/api/projects/YOUR-PROJECT
AZURE_AI_MODEL_DEPLOYMENT=gpt-4o
BING_CONNECTION_NAME=research-bing-grounding
```

### Step 6 — Login to Azure
```bash
az login
```

### Step 7 — Run the app
```bash
# Mac/Linux
./start.sh

# Windows
start.bat
```

### Step 8 — Open in browser
Go to **http://localhost:5173**

---

## 📁 Project Structure

```
research-intelligence-agent/
├── agents/
│   ├── orchestrator.py      # Master coordinator (Foundry IQ entry point)
│   ├── search_agent.py      # Source discovery via Grounding with Bing
│   ├── reader_agent.py      # Content extraction from web pages
│   ├── factcheck_agent.py   # Cross-referencing & contradiction detection
│   ├── synthesis_agent.py   # Final confidence-scored report generation
│   └── base_agent.py        # Azure AI Foundry base class (all agents)
├── tools/
│   ├── web_search.py        # Grounding with Bing Search integration
│   └── document_reader.py   # Web page content extractor
├── frontend/                # React web UI
│   ├── src/
│   │   ├── App.jsx          # Main UI with live agent progress
│   │   └── App.css          # Microsoft-themed dark UI
│   ├── index.html
│   └── package.json
├── outputs/                 # Generated reports saved here
├── app.py                   # FastAPI backend entry point
├── config.py                # Environment configuration
├── requirements.txt         # Python dependencies
├── .env.example             # Credentials template
├── start.sh                 # One-command startup (Mac/Linux)
├── start.bat                # One-command startup (Windows)
└── README.md
```

---

## 🔒 Safety & Reliability

- No confidential data processed or stored
- Input validation on all user queries
- Graceful error handling at every agent step — fallbacks if a source fails
- No hardcoded credentials — all via environment variables
- Managed Identity used for Azure authentication (no API keys stored)
- Confidence scores make uncertainty explicit — never presents guesses as facts
- Web content treated as untrusted input — validated before agent processing

---

## 🎥 Demo Video
[Link to be added on submission]

---

## 👤 Author
**Esvanth** | MSc Computing (AI), National College of Ireland  
Agents League Hackathon 2026 | Reasoning Agents Track | Foundry IQ
