from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Dict
import psutil

from models import SystemStatus, PolicyCheckRequest, PolicyCheckResponse, HealthResponse
from policies import check_system_health, validate_request_size, validate_http_method, enforce_rate_limit
from config import API_CONFIG, POLICY_RULES, RESOURCE_LIMITS

app = FastAPI(
    title=API_CONFIG["title"],
    version=API_CONFIG["version"],
    description=API_CONFIG["description"]
)

# In-memory storage for rate limiting
request_tracker: Dict[str, int] = {}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log all incoming and outgoing requests."""
    start_time = datetime.now()
    print(f"--> Incoming Request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = (datetime.now() - start_time).total_seconds()
    print(f"<-- Outgoing Response: Status {response.status_code} | Took {process_time:.4f}s")
    return response

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - basic health check"""
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(),
        service=API_CONFIG["title"]
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check endpoint"""
    status_str, _ = check_system_health()
    overall_status = "ok" if status_str != "critical" else "degraded"
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.now(),
        service=API_CONFIG["title"]
    )

@app.get("/status", response_model=SystemStatus)
async def get_system_status():
    """Get current system resource usage and status."""
    health_status, metrics = check_system_health()
    return SystemStatus(
        timestamp=datetime.now(),
        cpu_percent=metrics["cpu_percent"],
        memory_percent=metrics["memory_percent"],
        disk_percent=metrics["disk_percent"],
        status=health_status
    )

@app.post("/policy/check", response_model=PolicyCheckResponse)
async def check_policy(policy_request: PolicyCheckRequest):
    """Check if a request complies with defined policies."""
    # 1. Validate request size
    size_valid, size_msg = validate_request_size(policy_request.request_size)
    if not size_valid:
        return PolicyCheckResponse(allowed=False, reason=size_msg, policy_name="max_request_size")
        
    # 2. Validate HTTP method
    method_valid, method_msg = validate_http_method(policy_request.method)
    if not method_valid:
        return PolicyCheckResponse(allowed=False, reason=method_msg, policy_name="allowed_methods")
        
    # 3. Track and enforce rate limit
    user_id = policy_request.user_id
    current_count = request_tracker.get(user_id, 0) + 1
    request_tracker[user_id] = current_count
    
    rate_valid, rate_msg = enforce_rate_limit(user_id, current_count)
    if not rate_valid:
        return PolicyCheckResponse(allowed=False, reason=rate_msg, policy_name="rate_limit_per_minute")
        
    return PolicyCheckResponse(
        allowed=True,
        reason="All policy checks passed successfully.",
        policy_name="composite_policy_gate"
    )

@app.get("/policies")
async def list_policies():
    """List all active policy rules"""
    return POLICY_RULES

@app.get("/limits")
async def get_resource_limits():
    """Get configured resource limit thresholds"""
    return RESOURCE_LIMITS

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
