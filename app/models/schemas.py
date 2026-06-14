"""
Pydantic Models for Request/Response Validation
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    query: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Customer query or question"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "How long does a refund take?"
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    trace_id: str = Field(..., description="Unique request trace ID")
    status: Literal["success", "failed", "blocked"] = Field(
        ..., 
        description="Request status"
    )
    response: str = Field(..., description="Agent response")
    latency_seconds: float = Field(..., description="Request processing time")
    
    class Config:
        json_schema_extra = {
            "example": {
                "trace_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "success",
                "response": "Refunds typically take 5-7 business days to process.",
                "latency_seconds": 1.23
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: Literal["healthy", "unhealthy"] = Field(..., description="Service health status")
    version: str = Field(..., description="Application version")
    timestamp: str = Field(..., description="Current timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "2.0.0",
                "timestamp": "2026-06-14T09:18:00Z"
            }
        }


class ErrorResponse(BaseModel):
    """Response model for errors"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    trace_id: Optional[str] = Field(None, description="Request trace ID if available")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Internal server error",
                "detail": "An unexpected error occurred",
                "trace_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }

# Made with Bob
