import requests
import hmac
import hashlib
import json
from datetime import datetime

WEBHOOK_URL = "http://localhost:5000/webhook"
SECRET = "your-secret-key-change-this"

def send_webhook(payload, use_valid_signature=True):
    """Send a test webhook request with HMAC signatures."""
    payload_bytes = json.dumps(payload).encode()
    
    if use_valid_signature:
        signature = hmac.new(
            key=SECRET.encode(),
            msg=payload_bytes,
            digestmod=hashlib.sha256
        ).hexdigest()
    else:
        signature = "invalid_signature_hexdigest_123456"
    
    headers = {
        'Content-Type': 'application/json',
        'X-Hub-Signature-256': f'sha256={signature}'
    }
    
    try:
        response = requests.post(WEBHOOK_URL, data=payload_bytes, headers=headers, timeout=5)
        print(f"Status: {response.status_code} | Response: {response.json()}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    valid_payload = {
        "event": "user.created",
        "timestamp": datetime.utcnow().isoformat(),
        "data": {
            "user_id": "12345",
            "username": "testuser",
            "password": "super-secret-password-to-sanitize"
        }
    }
    
    print("Test 1: Sending valid webhook...")
    send_webhook(valid_payload, use_valid_signature=True)
    
    print("\nTest 2: Sending webhook with invalid signature...")
    send_webhook(valid_payload, use_valid_signature=False)
    
    invalid_payload = {
        "wrong_field": "value"
    }
    print("\nTest 3: Sending invalid payload schema...")
    send_webhook(invalid_payload, use_valid_signature=True)
