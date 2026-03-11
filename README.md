# Travel Planner — LangGraph Multi-Agent System

An AI-powered travel planning app that fetches live weather and generates personalised packing advice, places to visit, restaurant recommendations, and a full trip summary.

## Live Demo
**App**: https://security-agent-iq5w7vgj4a-uc.a.run.app  
**API Docs**: https://security-agent-iq5w7vgj4a-uc.a.run.app/docs


## What It Does
Enter any city and get:
- **Live weather** — temperature, humidity, wind speed
- **Packing advice** — based on current weather conditions
- **Top 5 places** — must-visit attractions
- **Top 5 restaurants** — best dining options
- **Full trip summary** — everything combined


## Tech Stack
- **LangGraph** — multi-agent pipeline
- **LLM Guard** — prompt injection protection
- **FastAPI** — REST API backend
- **OpenAI GPT-4o-mini** — AI responses
- **OpenWeatherMap API** — live weather data
- **GCP Cloud Run** — serverless deployment
- **Docker** — containerisation


## Architecture
```
User Input
    ↓
Weather Agent → Security Agent → Packing Agent → Security Agent
    → Trip Planner Agent → Security Agent → Restaurant Agent
    → Security Agent → Supervisor Agent
    ↓
Final Travel Brief
```

The **Security Agent** runs between every agent hop to:
- Detect prompt injection attacks (LLM Guard + regex)
- Sanitise all state fields
- Verify HMAC signatures for tamper detection

## Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/priya-bellamkonda/Travel-agent.git
cd Travel-agent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add API keys — create a .env file**
```
OPENAI_API_KEY=sk-proj-...
OPENWEATHER_API_KEY=your-key
```

**4. Run**
```bash
uvicorn api:app --reload
```

**5. Open browser**
```
http://localhost:8000
```


## Deploy to GCP Cloud Run
```bash
bash deploy.sh
```


## Project Structure
```
Travel-agent/
├── api.py                  ← FastAPI web server
├── main.py                 ← Terminal version
├── graph.py                ← LangGraph pipeline
├── state.py                ← Shared agent state
├── Dockerfile              ← Container config
├── deploy.sh               ← GCP deployment script
├── agents/
│   ├── weather_agent.py
│   ├── packing_agent.py
│   ├── trip_planner_agent.py
│   ├── restaurant_agent.py
│   ├── supervisor_agent.py
│   └── security_agent.py
├── skills/
│   ├── weather_skill.py
│   ├── packing_skill.py
│   ├── trip_planner_skill.py
│   ├── restaurant_skill.py
│   ├── supervisor_skill.py
│   └── security_skill.py
└── static/
    └── index.html          ← Frontend UI
```


## Security
- API keys stored in **GCP Secret Manager** — never in code
- **LLM Guard** ML model detects prompt injection attacks
- **HMAC signatures** verify state integrity between agents
- `.env` excluded from GitHub via `.gitignore`
