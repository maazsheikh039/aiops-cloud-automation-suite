from resilient_client import ResilientHTTPClient
import json

def test_successful_request():
    """Test basic successful request."""
    print("\n=== Test 1: Successful Request ===")
    client = ResilientHTTPClient(max_retries=3, base_timeout=10)
    try:
        response = client.get("https://httpbin.org/get")
        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json().get('url')}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

def test_timeout_handling():
    """Test timeout with retry."""
    print("\n=== Test 2: Timeout Handling ===")
    client = ResilientHTTPClient(max_retries=2, base_timeout=1)
    try:
        # Requesting a 3-second delay with a 1-second timeout should trigger timeout/retry
        response = client.get("https://httpbin.org/delay/3")
        print(f"Success: Status {response.status_code}")
    except Exception as e:
        print(f"Caught expected timeout exception after retries: {e}")
    finally:
        client.close()

def test_retry_on_failure():
    """Test retry on connection failure."""
    print("\n=== Test 3: Retry on Failure ===")
    client = ResilientHTTPClient(max_retries=2, base_timeout=2)
    try:
        client.get("http://invalid-domain-12345.com")
    except Exception as e:
        print(f"Caught expected connection failure after retries: {e}")
    finally:
        client.close()

def test_post_request():
    """Test POST request with data."""
    print("\n=== Test 4: POST Request ===")
    client = ResilientHTTPClient(max_retries=3, base_timeout=10)
    payload = {"task": "AIOps Lab", "status": "Resilient"}
    try:
        response = client.post("https://httpbin.org/post", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Echoed JSON: {response.json().get('json')}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    test_successful_request()
    test_timeout_handling()
    test_retry_on_failure()
    test_post_request()
