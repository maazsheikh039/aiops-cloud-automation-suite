from typing import Dict, Tuple
from config import RESOURCE_LIMITS, POLICY_RULES
import psutil

def check_system_health() -> Tuple[str, Dict[str, float]]:
    """
    Check system resource usage and determine health status.
    
    Returns:
        Tuple of (status_string, metrics_dict)
        status can be: "healthy", "warning", "critical"
    """
    cpu = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    metrics = {
        "cpu_percent": cpu,
        "memory_percent": memory,
        "disk_percent": disk
    }
    
    # Check against limits
    if (cpu > RESOURCE_LIMITS["cpu_percent"] or 
        memory > RESOURCE_LIMITS["memory_percent"] or 
        disk > RESOURCE_LIMITS["disk_percent"]):
        status = "critical"
    elif (cpu > 70.0 or memory > 70.0 or disk > 70.0):
        status = "warning"
    else:
        status = "healthy"
        
    return status, metrics

def validate_request_size(size_bytes: int) -> Tuple[bool, str]:
    """Validate if request size is within policy limits."""
    max_size = POLICY_RULES["max_request_size"]
    if size_bytes > max_size:
        return False, f"Request size {size_bytes} bytes exceeds maximum allowed limit of {max_size} bytes."
    return True, "Request size is within acceptable limits."

def validate_http_method(method: str) -> Tuple[bool, str]:
    """Validate if HTTP method is allowed by policy."""
    upper_method = method.upper()
    allowed = POLICY_RULES["allowed_methods"]
    if upper_method not in allowed:
        return False, f"HTTP method '{method}' is not allowed. Allowed methods: {allowed}"
    return True, "HTTP method is permitted."

def enforce_rate_limit(user_id: str, request_count: int) -> Tuple[bool, str]:
    """Check if user has exceeded rate limit."""
    limit = POLICY_RULES["rate_limit_per_minute"]
    if request_count > limit:
        return False, f"User '{user_id}' has exceeded rate limit of {limit} requests per minute."
    return True, "Rate limit check passed."
