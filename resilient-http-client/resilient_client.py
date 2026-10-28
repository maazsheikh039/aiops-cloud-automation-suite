import requests
import time
import logging
from typing import Optional, Dict, Any
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ResilientHTTPClient")

class ResilientHTTPClient:
    """
    A resilient HTTP client with retry logic, backoff, and timeout handling.
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        base_timeout: int = 5,
        backoff_factor: float = 2.0,
        use_circuit_breaker: bool = False
    ):
        self.max_retries = max_retries
        self.base_timeout = base_timeout
        self.backoff_factor = backoff_factor
        self.session = requests.Session()
        
        # Optional circuit breaker integration
        if use_circuit_breaker:
            from circuit_breaker import CircuitBreaker
            self.circuit_breaker = CircuitBreaker()
        else:
            self.circuit_breaker = None
    
    def _calculate_backoff(self, attempt: int) -> float:
        """Calculate exponential backoff delay: base_delay * (backoff_factor ^ attempt)"""
        base_delay = 1.0
        delay = base_delay * (self.backoff_factor ** attempt)
        return delay
    
    def _should_retry(self, exception: Exception, attempt: int) -> bool:
        """Determine if request should be retried based on exception type and status code."""
        if attempt >= self.max_retries:
            return False
            
        if isinstance(exception, (Timeout, ConnectionError)):
            return True
            
        if isinstance(exception, HTTPError) and exception.response is not None:
            status_code = exception.response.status_code
            # Retry on rate limit (429) and server errors (500, 502, 503, 504)
            if status_code == 429 or (500 <= status_code < 600):
                return True
                
        return False
    
    def _get_with_retry(self, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """Internal GET execution with retry loop."""
        for attempt in range(self.max_retries + 1):
            try:
                logger.info(f"GET Request to {url} (Attempt {attempt + 1}/{self.max_retries + 1})")
                response = self.session.get(url, params=params, headers=headers, timeout=self.base_timeout)
                
                # Raise HTTPError for bad status codes to trigger retry logic if needed
                if response.status_code == 429 or (500 <= response.status_code < 600):
                    http_err = HTTPError(f"Server error status {response.status_code}", response=response)
                    raise http_err
                    
                response.raise_for_status()
                return response
                
            except (Timeout, ConnectionError, HTTPError) as e:
                if self._should_retry(e, attempt):
                    delay = self._calculate_backoff(attempt)
                    logger.warning(f"Request failed due to {e}. Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"Request permanently failed after attempt {attempt + 1}: {e}")
                    raise
            except RequestException as e:
                logger.error(f"Non-retryable request exception: {e}")
                raise

    def get(self, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """Perform a GET request with retry logic (and optional circuit breaker)."""
        if self.circuit_breaker:
            return self.circuit_breaker.call(self._get_with_retry, url, params, headers)
        else:
            return self._get_with_retry(url, params, headers)
    
    def _post_with_retry(self, url: str, data: Optional[Dict[str, Any]] = None, json_payload: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """Internal POST execution with retry loop."""
        for attempt in range(self.max_retries + 1):
            try:
                logger.info(f"POST Request to {url} (Attempt {attempt + 1}/{self.max_retries + 1})")
                response = self.session.post(url, data=data, json=json_payload, headers=headers, timeout=self.base_timeout)
                
                if response.status_code == 429 or (500 <= response.status_code < 600):
                    http_err = HTTPError(f"Server error status {response.status_code}", response=response)
                    raise http_err
                    
                response.raise_for_status()
                return response
                
            except (Timeout, ConnectionError, HTTPError) as e:
                if self._should_retry(e, attempt):
                    delay = self._calculate_backoff(attempt)
                    logger.warning(f"POST failed due to {e}. Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"POST permanently failed after attempt {attempt + 1}: {e}")
                    raise
            except RequestException as e:
                logger.error(f"Non-retryable POST exception: {e}")
                raise

    def post(self, url: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """Perform a POST request with retry logic."""
        if self.circuit_breaker:
            return self.circuit_breaker.call(self._post_with_retry, url, data, json, headers)
        else:
            return self._post_with_retry(url, data, json, headers)
    
    def close(self):
        """Close the session."""
        self.session.close()
