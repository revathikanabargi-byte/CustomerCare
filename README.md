# CustomerCare
Enterprise AI Customer Support Agent

## 🔒 Security Notice

This repository has been updated to remove hardcoded API keys. All sensitive credentials must now be stored in environment variables.

## ✨ What's New in v2.0

The project now features a **clean, production-ready FastAPI architecture** with:

- 🏗️ **Modular Structure**: Separation of concerns with dedicated modules
- 🔌 **RESTful API**: Clean API endpoints with OpenAPI documentation
- 🛡️ **Enhanced Security**: CORS, input validation, and safety checks
- 📊 **Better Observability**: Structured logging and request tracing
- 🚀 **Easy Deployment**: Multiple deployment options (Docker, Cloud, etc.)
- 📝 **Comprehensive Docs**: Interactive API docs and deployment guides

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd CustomerCare
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_actual_api_key_here
```

**⚠️ IMPORTANT:**
- Never commit the `.env` file to version control
- Get your API key from: https://platform.openai.com/api-keys
- Keep your API key secure and private

### 5. Run the Application

**Production FastAPI Application (Recommended):**
```bash
# Option 1: Using startup script
python run.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload

# Option 3: Using Python module
python -m app.main
```

**Legacy Phase Scripts (For Learning):**
```bash
# Phase 3: Smart Agent with LLM Integration
python ph3_smart_agent_llm_integration.py

# Phase 4: Knowledge Retrieval (RAG)
python ph4_knowledge_retreival.py

# Phase 5: Tool Usage
python ph5_tool_usage.py

# Phase 6: Planning, Memory & Context
python ph6_planning_memory_context.py

# Phase 7: Adaptive Behaviour
python ph7_adaptive_behaviour.py

# Phase 8: Deployable Agent (Legacy)
uvicorn ph8_deployable_agent:app --reload

# Phase 9: Evaluation
python ph9_evaluation.py
```

### 6. Access the Application

Once running, access:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📋 Project Structure

```
CustomerCare/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py             # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py             # Configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py            # Pydantic models
│   └── services/
│       ├── __init__.py
│       └── agent_service.py      # Business logic
├── .env                          # Environment variables (DO NOT COMMIT)
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── run.py                        # Startup script
├── knowledge_base.txt            # Knowledge base for RAG
├── DEPLOYMENT.md                 # Deployment guide
├── README.md                     # This file
├── SECURITY.md                   # Security guidelines
├── ph3_smart_agent_llm_integration.py  # Learning phases
├── ph4_knowledge_retreival.py
├── ph5_tool_usage.py
├── ph6_planning_memory_context.py
├── ph7_adaptive_behaviour.py
├── ph8_deployable_agent.py       # Legacy deployment
└── ph9_evaluation.py
```

## 🛡️ Security Best Practices

1. **Never commit sensitive data** - API keys, passwords, tokens
2. **Use environment variables** - Store secrets in `.env` file
3. **Keep `.env` in .gitignore** - Prevent accidental commits
4. **Rotate API keys regularly** - Especially if exposed
5. **Use `.env.example`** - Share template without secrets

## 📚 Features

- **LLM Integration**: OpenAI GPT-4 powered responses
- **RAG (Retrieval-Augmented Generation)**: Knowledge base grounding
- **Tool Usage**: Extensible tool framework
- **Memory & Context**: Multi-turn conversation support
- **Adaptive Behavior**: Learning from feedback
- **Production Ready**: FastAPI deployment with logging
- **Evaluation Framework**: Automated testing and metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure `.env` is not committed
5. Submit a pull request

## 📄 License

[Add your license here]


## 🔌 API Endpoints

### Health Check
```http
GET /health
```

### Chat with Agent
```http
POST /chat
Content-Type: application/json

{
  "query": "How long does a refund take?"
}
```

### Clear Conversation Memory
```http
POST /clear-memory
```

### Application Info
```http
GET /info
```

For detailed API documentation, see the interactive docs at `/docs` when running.

## 🐳 Deployment

### Local Development
```bash
python run.py
```

### Docker
```bash
docker build -t customer-care-agent .
docker run -p 8000:8000 --env-file .env customer-care-agent
```

### Cloud Platforms
- **AWS**: Elastic Beanstalk, ECS, Lambda
- **Azure**: App Service, Container Instances
- **GCP**: Cloud Run, App Engine
- **Heroku**: Direct deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

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

### Interactive Testing
Visit http://localhost:8000/docs for Swagger UI with interactive API testing.

## 📖 Documentation

- **README.md** (this file): Quick start and overview
- **DEPLOYMENT.md**: Comprehensive deployment guide
- **SECURITY.md**: Security guidelines and best practices
- **/docs**: Interactive API documentation (when running)
- **/redoc**: Alternative API documentation (when running)

## 🔧 Configuration

Configuration is managed through environment variables and `app/core/config.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | OpenAI API key |
| `OPENAI_MODEL` | gpt-4o-mini | Model to use |
| `OPENAI_TEMPERATURE` | 0.0 | Response randomness |
| `KNOWLEDGE_BASE_PATH` | knowledge_base.txt | Path to KB file |
| `MAX_CONVERSATION_MEMORY` | 5 | Max conversation turns |
| `LOG_LEVEL` | INFO | Logging level |

## 📝 Changelog

### v2.0.0 (Current)
- ✨ Complete FastAPI rewrite with modular architecture
- 🏗️ Separated concerns: routes, services, models, config
- 🔌 RESTful API with OpenAPI documentation
- 🛡️ Enhanced security and validation
- 📊 Improved logging and observability
- 🚀 Multiple deployment options

### v1.0.0 (Legacy)
- Initial implementation with phase-based learning scripts
- Basic FastAPI deployment in ph8_deployable_agent.py

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [LangChain](https://www.langchain.com/)
- LLM by [OpenAI](https://openai.com/)
