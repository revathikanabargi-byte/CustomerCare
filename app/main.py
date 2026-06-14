"""
Customer Care AI Agent - FastAPI Application
Main application entry point with middleware and configuration
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings, validate_settings
from app.api.routes import router

# Configure logging
logging.basicConfig(
    filename=settings.log_file,
    level=getattr(logging, settings.log_level),
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("Starting Customer Care AI Agent...")
    try:
        validate_settings()
        logger.info("Configuration validated successfully")
        logger.info(f"Application version: {settings.app_version}")
        logger.info(f"OpenAI model: {settings.openai_model}")
        logger.info(f"Knowledge base: {settings.knowledge_base_path}")
    except Exception as e:
        logger.error(f"Startup validation failed: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Customer Care AI Agent...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    Enterprise-grade AI Customer Support Agent with:
    
    * **RAG (Retrieval-Augmented Generation)** - Grounded responses from knowledge base
    * **Conversation Memory** - Context-aware multi-turn conversations
    * **Safety Checks** - Built-in security and content filtering
    * **Request Tracing** - Full observability with trace IDs
    * **Graceful Error Handling** - Production-ready error responses
    * **Health Monitoring** - Service health check endpoint
    
    ## Quick Start
    
    1. Use `/chat` endpoint to send customer queries
    2. Check `/health` for service status
    3. Use `/clear-memory` to reset conversation context
    
    ## Authentication
    
    Currently no authentication required (add as needed for production)
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# Custom exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred. Please try again later."
        }
    )


# Include API routes
app.include_router(router, tags=["Customer Care Agent"])


# Application metadata
@app.get("/info", tags=["Metadata"])
async def app_info():
    """Get application information"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "model": settings.openai_model,
        "knowledge_base": settings.knowledge_base_path,
        "max_memory": settings.max_conversation_memory
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

# Made with Bob
