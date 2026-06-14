"""
API Routes for Customer Care Agent
"""

import time
import uuid
import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    ErrorResponse
)
from app.services.agent_service import agent_service
from app.core.config import settings

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the service is healthy and running"
)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with Agent",
    description="Send a customer query and receive an AI-generated response",
    responses={
        200: {"description": "Successful response"},
        400: {"model": ErrorResponse, "description": "Bad request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def chat(request: ChatRequest):
    """
    Chat endpoint for customer queries
    
    - **query**: Customer question or issue (1-1000 characters)
    
    Returns:
    - **trace_id**: Unique identifier for request tracing
    - **status**: Request status (success/failed/blocked)
    - **response**: Agent's response to the query
    - **latency_seconds**: Time taken to process the request
    """
    trace_id = str(uuid.uuid4())
    start_time = time.time()
    
    try:
        # Validate query length
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query cannot be empty"
            )
        
        query = request.query.strip()
        
        # Add to memory
        agent_service.add_to_memory("Customer", query)
        
        # Generate response
        result = agent_service.generate_response(query)
        
        # Add response to memory
        if result["status"] == "success":
            agent_service.add_to_memory("Agent", result["response"])
        
        # Calculate latency
        latency = round(time.time() - start_time, 2)
        
        # Log request
        logger.info(
            f"TRACE_ID={trace_id} | "
            f"QUERY={query[:100]} | "
            f"STATUS={result['status']} | "
            f"LATENCY={latency}s"
        )
        
        return ChatResponse(
            trace_id=trace_id,
            status=result["status"],
            response=result["response"],
            latency_seconds=latency
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        latency = round(time.time() - start_time, 2)
        
        # Log error
        logger.error(
            f"TRACE_ID={trace_id} | "
            f"STATUS=FAILED | "
            f"LATENCY={latency}s | "
            f"ERROR={str(e)}"
        )
        
        # Return graceful error response
        return ChatResponse(
            trace_id=trace_id,
            status="failed",
            response=(
                "The support agent encountered a temporary issue. "
                "Please try again later or contact human support."
            ),
            latency_seconds=latency
        )


@router.post(
    "/clear-memory",
    summary="Clear Conversation Memory",
    description="Clear the conversation memory for a fresh start"
)
async def clear_memory():
    """Clear conversation memory endpoint"""
    try:
        agent_service.clear_memory()
        return {"message": "Conversation memory cleared successfully"}
    except Exception as e:
        logger.error(f"Failed to clear memory: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear conversation memory"
        )


@router.get(
    "/",
    summary="Root Endpoint",
    description="Welcome message and API information"
)
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }

# Made with Bob
