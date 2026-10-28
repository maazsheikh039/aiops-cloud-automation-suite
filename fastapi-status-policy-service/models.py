from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class SystemStatus(BaseModel):
    """Model for system status response"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    status: str  # "healthy", "warning", "critical"

class PolicyCheckRequest(BaseModel):
    """Model for policy check requests"""
    request_size: int = Field(..., description="Request size in bytes")
    method: str = Field(..., description="HTTP method")
    user_id: str = Field(..., description="User identifier")

class PolicyCheckResponse(BaseModel):
    """Model for policy check responses"""
    allowed: bool = Field(..., description="Whether the request complies with policies")
    reason: str = Field(..., description="Explanation for policy decision")
    policy_name: str = Field(..., description="Name or type of policy evaluated")

class HealthResponse(BaseModel):
    """Model for health check response"""
    status: str
    timestamp: datetime
    service: str = "FastAPI Policy Service"
