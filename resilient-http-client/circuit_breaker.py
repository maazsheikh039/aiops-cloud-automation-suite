from enum import Enum
import time
import logging

logger = logging.getLogger("CircuitBreaker")

class CircuitState(Enum):
    CLOSED = "closed"          # Normal operation
    OPEN = "open"              # Failing, reject requests
    HALF_OPEN = "half_open"      # Testing if recovered

class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is OPEN and rejects execution."""
    pass

class CircuitBreaker:
    """
    Implements circuit breaker pattern to prevent cascading failures.
    """
    
    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: int = 10,
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
    
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        now = time.time()
        
        # Check if OPEN state should transition to HALF_OPEN
        if self.state == CircuitState.OPEN:
            if self.last_failure_time and (now - self.last_failure_time) > self.recovery_timeout:
                logger.info("Circuit breaker recovery timeout elapsed. Transitioning from OPEN to HALF_OPEN.")
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise CircuitBreakerOpenError("Circuit breaker is OPEN. Request rejected.")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Handle successful call."""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            logger.info(f"Circuit breaker HALF_OPEN success count: {self.success_count}/{self.success_threshold}")
            if self.success_count >= self.success_threshold:
                logger.info("Circuit breaker recovered successfully. Transitioning to CLOSED.")
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
        elif self.state == CircuitState.CLOSED:
            # Reset failures on success during normal operation
            self.failure_count = 0
    
    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        logger.warning(f"Circuit breaker failure recorded. Count: {self.failure_count}/{self.failure_threshold}")
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("Failure detected in HALF_OPEN state. Re-opening circuit.")
            self.state = CircuitState.OPEN
        elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
            logger.error("Failure threshold reached. Opening circuit breaker!")
            self.state = CircuitState.OPEN
