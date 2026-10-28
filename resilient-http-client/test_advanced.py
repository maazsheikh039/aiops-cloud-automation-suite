from resilient_client import ResilientHTTPClient
from circuit_breaker import CircuitBreakerOpenError
import time

def test_circuit_breaker():
    """Test circuit breaker functionality."""
    print("\n=== Circuit Breaker Test ===")
    # Client with circuit breaker enabled
    client = ResilientHTTPClient(max_retries=1, base_timeout=2, use_circuit_breaker=True)
    
    # Hit an invalid endpoint repeatedly to trip the circuit breaker (threshold = 3 failures)
    for i in range(4):
        try:
            print(f"Attempt {i+1} to invalid domain:")
            client.get("http://nonexistent-domain-xyz-987.com")
        except Exception as e:
            print(f"  -> Caught error: {type(e).__name__}")
        time.sleep(0.5)
        
    # Subsequent call should be instantly rejected by Circuit Breaker OPEN state
    print("\nTesting subsequent call while Circuit Breaker is OPEN:")
    try:
        client.get("https://httpbin.org/get")
    except CircuitBreakerOpenError as cb_err:
        print(f"  -> Success: Circuit Breaker blocked request! ({cb_err})")
    except Exception as e:
        print(f"  -> Unexpected error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    test_circuit_breaker()
