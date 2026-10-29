from flask import Flask, request, jsonify
import hmac
import hashlib
import json
import logging
from datetime import datetime
from jsonschema import validate, ValidationError

app = Flask(__name__)

# Configuration
WEBHOOK_SECRET = "your-secret-key-change-this"
LOG_FILE = "webhook_events.log"

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def verify_signature(payload_body, signature_header):
    """
    Verify the webhook signature using HMAC-SHA256 with constant-time comparison.
    """
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    
    provided_sig = signature_header.split("=")[1]
    
    computed_sig = hmac.new(
        key=WEBHOOK_SECRET.encode(),
        msg=payload_body,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(computed_sig, provided_sig)

def validate_payload(payload):
    """
    Validate webhook payload against expected schema.
    """
    schema = {
        "type": "object",
        "properties": {
            "event": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["event", "timestamp", "data"]
    }
    
    try:
        validate(instance=payload, schema=schema)
        return True
    except ValidationError as e:
        logging.error(f"Payload validation failed: {e.message}")
        return False

def log_webhook_event(event_type, payload, status):
    """
    Log webhook event details securely while sanitizing sensitive keys.
    """
    # Sanitize payload data to remove sensitive fields
    sanitized_data = {}
    if isinstance(payload.get('data'), dict):
        sanitized_data = {
            k: v for k, v in payload['data'].items() 
            if k.lower() not in ['password', 'secret', 'token', 'api_key', 'auth']
        }

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "status": status,
        "payload_summary": sanitized_data
    }
    logging.info(json.dumps(log_entry))

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """
    Main webhook endpoint handler with authentication, validation, and processing.
    """
    signature_header = request.headers.get('X-Hub-Signature-256')
    raw_payload = request.get_data()
    
    # 1. Verify HMAC Signature
    if not verify_signature(raw_payload, signature_header):
        log_webhook_event("unknown", {}, "failure_invalid_signature")
        return jsonify({"error": "Invalid signature"}), 401
        
    # 2. Parse JSON
    try:
        payload = request.get_json(force=True)
    except Exception as e:
        log_webhook_event("unknown", {}, "failure_invalid_json")
        return jsonify({"error": "Invalid JSON format"}), 400
        
    # 3. Validate Schema
    if not validate_payload(payload):
        log_webhook_event(payload.get('event', 'unknown'), payload, "failure_invalid_schema")
        return jsonify({"error": "Payload schema validation failed"}), 400
        
    # 4. Process Event & Log Success
    event_type = payload.get('event')
    log_webhook_event(event_type, payload, "success")
    
    return jsonify({"status": "received", "event": event_type}), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
