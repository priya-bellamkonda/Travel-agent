set -e

# Config 
PROJECT_ID="security-agent-489907"
REGION="us-central1"
SERVICE_NAME="security-agent"
IMAGE="us-central1-docker.pkg.dev/${PROJECT_ID}/${SERVICE_NAME}/${SERVICE_NAME}"

# Read API keys from .env file (never hardcode secrets!) 
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
  echo ">>> Loaded API keys from .env file"
else
  echo "ERROR: .env file not found!"
  echo "Create a .env file with:"
  echo "  OPENAI_API_KEY=sk-proj-..."
  echo "  OPENWEATHER_API_KEY=your-key"
  exit 1
fi

# Validate keys are set 
if [ -z "$OPENAI_API_KEY" ]; then
  echo "ERROR: OPENAI_API_KEY is not set in .env"
  exit 1
fi

if [ -z "$OPENWEATHER_API_KEY" ]; then
  echo "ERROR: OPENWEATHER_API_KEY is not set in .env"
  exit 1
fi

# 1. Set project 
echo ">>> Setting GCP project..."
gcloud config set project "$PROJECT_ID"

# 2. Enable APIs 
echo ">>> Enabling APIs..."
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  secretmanager.googleapis.com \
  artifactregistry.googleapis.com

# 3. Create Artifact Registry repo (first time only) 
echo ">>> Creating Artifact Registry repository..."
gcloud artifacts repositories create "$SERVICE_NAME" \
  --repository-format=docker \
  --location="$REGION" 2>/dev/null || echo "Repository already exists, skipping."

# 4. Store secrets in Secret Manager (never in code!) 
echo ">>> Storing secrets in Secret Manager..."
echo -n "$OPENAI_API_KEY" | gcloud secrets create openai-api-key \
  --data-file=- 2>/dev/null || \
  echo -n "$OPENAI_API_KEY" | gcloud secrets versions add openai-api-key --data-file=-

echo -n "$OPENWEATHER_API_KEY" | gcloud secrets create openweather-api-key \
  --data-file=- 2>/dev/null || \
  echo -n "$OPENWEATHER_API_KEY" | gcloud secrets versions add openweather-api-key --data-file=-

# 5. Build & push image 
echo ">>> Building image with Cloud Build..."
gcloud builds submit --tag "$IMAGE" .

# 6. Deploy to Cloud Run 
echo ">>> Deploying to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
  --image "$IMAGE" \
  --platform managed \
  --region "$REGION" \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 120 \
  --set-secrets "OPENAI_API_KEY=openai-api-key:latest,OPENWEATHER_API_KEY=openweather-api-key:latest"

# 7. Print service URL 
echo ""
echo ">>> Deployment complete!"
gcloud run services describe "$SERVICE_NAME" \
  --region "$REGION" \
  --format "value(status.url)"