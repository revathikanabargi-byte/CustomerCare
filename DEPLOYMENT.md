# Customer Care AI Agent - Deployment Guide

## 🏗️ Architecture Overview

The application follows a clean, modular architecture:

```
app/
├── __init__.py              # Package initialization
├── main.py                  # FastAPI application entry point
├── api/
│   ├── __init__.py
│   └── routes.py            # API endpoints
├── core/
│   ├── __init__.py
│   └── config.py            # Configuration management
├── models/
│   ├── __init__.py
│   └── schemas.py           # Pydantic models
└── services/
    ├── __init__.py
    └── agent_service.py     # Business logic
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Virtual environment (recommended)

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd CustomerCare

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_api_key_here
```

### 4. Run the Application

**Option 1: Using the startup script (Recommended)**
```bash
python run.py
```

**Option 2: Using uvicorn directly**
```bash
uvicorn app.main:app --reload
```

**Option 3: Using the main module**
```bash
python -m app.main
```

The application will start on `http://localhost:8000`

## 📚 API Documentation

Once running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": "2026-06-14T09:00:00Z"
}
```

### Chat
```http
POST /chat
Content-Type: application/json

{
  "query": "How long does a refund take?"
}
```

**Response:**
```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "response": "Refunds typically take 5-7 business days to process...",
  "latency_seconds": 1.23
}
```

### Clear Memory
```http
POST /clear-memory
```

**Response:**
```json
{
  "message": "Conversation memory cleared successfully"
}
```

### Application Info
```http
GET /info
```

**Response:**
```json
{
  "name": "Customer Care AI Agent",
  "version": "2.0.0",
  "model": "gpt-4o-mini",
  "knowledge_base": "knowledge_base.txt",
  "max_memory": 5
}
```

## 🐳 Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run

```bash
# Build image
docker build -t customer-care-agent .

# Run container
docker run -d -p 8000:8000 --env-file .env customer-care-agent
```

## ☁️ Cloud Deployment

### AWS (Elastic Beanstalk)

1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init -p python-3.11 customer-care-agent`
3. Create environment: `eb create customer-care-env`
4. Deploy: `eb deploy`

### Azure (App Service)

```bash
az webapp up --name customer-care-agent --runtime "PYTHON:3.11"
```

### Google Cloud (Cloud Run)

```bash
gcloud run deploy customer-care-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Heroku

```bash
heroku create customer-care-agent
git push heroku main
```

## 🔒 Production Considerations

### Security

1. **Environment Variables**: Never commit `.env` file
2. **API Keys**: Rotate regularly, use secrets management
3. **CORS**: Configure `cors_origins` in config for specific domains
4. **Rate Limiting**: Add rate limiting middleware
5. **Authentication**: Implement OAuth2 or API key authentication

### Performance

1. **Caching**: Add Redis for conversation memory
2. **Database**: Use PostgreSQL for persistent storage
3. **Load Balancing**: Deploy multiple instances behind load balancer
4. **CDN**: Use CDN for static assets

### Monitoring

1. **Logging**: Configure structured logging (JSON format)
2. **Metrics**: Add Prometheus metrics
3. **Tracing**: Integrate OpenTelemetry or LangSmith
4. **Alerts**: Set up alerts for errors and latency

### Scaling

```bash
# Kubernetes deployment
kubectl apply -f k8s/deployment.yaml
kubectl scale deployment customer-care-agent --replicas=3
```

## 🧪 Testing

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I reset my password?"}'
```

### Load Testing

```bash
# Using Apache Bench
ab -n 1000 -c 10 -p query.json -T application/json http://localhost:8000/chat

# Using wrk
wrk -t4 -c100 -d30s http://localhost:8000/health
```

## 📊 Configuration Options

Edit `app/core/config.py` or set environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | OpenAI API key |
| `OPENAI_MODEL` | gpt-4o-mini | Model to use |
| `OPENAI_TEMPERATURE` | 0.0 | Response randomness |
| `KNOWLEDGE_BASE_PATH` | knowledge_base.txt | Path to KB file |
| `MAX_CONVERSATION_MEMORY` | 5 | Max conversation turns |
| `LOG_LEVEL` | INFO | Logging level |

## 🔧 Troubleshooting

### Common Issues

**Issue**: `OPENAI_API_KEY not found`
- **Solution**: Create `.env` file with your API key

**Issue**: `knowledge_base.txt not found`
- **Solution**: Ensure file exists in root directory

**Issue**: Import errors
- **Solution**: Reinstall dependencies: `pip install -r requirements.txt`

**Issue**: Port already in use
- **Solution**: Change port: `uvicorn app.main:app --port 8001`

## 📝 Logs

Logs are written to `app.log` in the root directory. Configure log level in `.env`:

```env
LOG_LEVEL=DEBUG
```

## 🔄 Updates and Maintenance

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Database Migrations

(Add when database is implemented)

### Backup

Backup the following:
- `.env` file (securely)
- `knowledge_base.txt`
- `app.log` (for analysis)
- Conversation memory (if persisted)

## 📞 Support

For issues or questions:
- Check logs in `app.log`
- Review API documentation at `/docs`
- Check trace IDs in error responses

## 📄 License

[Add your license here]