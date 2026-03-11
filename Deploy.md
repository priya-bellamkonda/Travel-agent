# Deploying to Google Cloud Run

## Prerequisites
1. [Install Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. [Create a GCP project](https://console.cloud.google.com/)
3. Enable billing on your GCP project
4. Install Docker Desktop (for local testing only)

---

## Step 1 — Authenticate with GCP
```bash
gcloud auth login
gcloud auth configure-docker
```

---

## Step 2 — Edit deploy.sh
Open `deploy.sh` and set your values:
```bash
PROJECT_ID="your-actual-project-id"   # from GCP console
REGION="us-central1"                   # or europe-west1 etc.
SERVICE_NAME="travel-planner"          # name for your Cloud Run service
```

---

## Step 3 — Set your API keys as environment variables
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-proj-..."
$env:OPENWEATHER_API_KEY="4a80db52..."

# Mac/Linux
export OPENAI_API_KEY="sk-proj-..."
export OPENWEATHER_API_KEY="4a80db52..."
```

---

## Step 4 — Deploy
```bash
# Mac/Linux
bash deploy.sh

# Windows (use Git Bash or WSL)
bash deploy.sh
```

This will:
- Store your API keys securely in GCP Secret Manager
- Build your Docker image using Cloud Build
- Deploy to Cloud Run with 1GB RAM, 120s timeout
- Print your live URL when done

---

## Step 5 — Test your live API

### Health check
```bash
curl https://your-service-url/health
```

### Plan a trip
```bash
curl -X POST https://your-service-url/plan \
  -H "Content-Type: application/json" \
  -d '{"city": "Dublin"}'
```

---

## Test locally with Docker first
```bash
docker build -t travel-planner .
docker run -p 8080:8080 \
  -e OPENAI_API_KEY="sk-proj-..." \
  -e OPENWEATHER_API_KEY="4a80db52..." \
  travel-planner
```
Then visit: http://localhost:8080/docs (Swagger UI)

---

## API Endpoints

| Method | Endpoint  | Description                        |
|--------|-----------|------------------------------------|
| GET    | /health   | Health check + LLM Guard status    |
| POST   | /plan     | Run the full travel planning pipeline |
| GET    | /docs     | Swagger UI (auto-generated)        |

### POST /plan request body
```json
{ "city": "Dublin" }
```

### POST /plan response
```json
{
  "city": "Dublin",
  "weather_report": "...",
  "packing_advice": "...",
  "activity_suggestions": "...",
  "restaurant_suggestions": "...",
  "final_summary": "..."
}
```

---

## LLM Guard — Prompt Injection Protection
The security skill now runs every city input through two layers:
1. **Regex patterns** — catches known injection phrases instantly
2. **LLM Guard PromptInjection scanner** — ML-based detection for subtle attacks

Example blocked inputs:
- `"ignore all previous instructions"`
- `"act as a different AI"`
- `"<script>alert('xss')</script>"`

The `/health` endpoint tells you if LLM Guard loaded successfully.