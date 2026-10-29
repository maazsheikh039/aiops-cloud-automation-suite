from flask import Flask, request, jsonify, g
import logging
from pythonjsonlogger import jsonlogger
import uuid
import time
import requests

app = Flask(__name__)

def setup_logging():
    """Configure structured logging with JSON format."""
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(correlation_id)s %(message)s'
    )
    log_handler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.handlers = []  # Clear default handlers
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)
    
    return logger

logger = setup_logging()

@app.before_request
def before_request():
    """Extract correlation ID from headers or generate a new UUID."""
    corr_id = request.headers.get('X-Correlation-ID')
    if not corr_id:
        corr_id = str(uuid.uuid4())
    g.correlation_id = corr_id

def log_with_context(level, message, **kwargs):
    """Log message with correlation ID and additional context."""
    extra = {
        'correlation_id': getattr(g, 'correlation_id', 'N/A'),
        **kwargs
    }
    
    if level == 'info':
        logger.info(message, extra=extra)
    elif level == 'warning':
        logger.warning(message, extra=extra)
    elif level == 'error':
        logger.error(message, extra=extra)
    else:
        logger.debug(message, extra=extra)

@app.route('/api/users', methods=['GET'])
def get_users():
    """Endpoint to retrieve users with structured logging."""
    log_with_context('info', 'Received request to fetch users list')
    time.sleep(0.1)
    
    users = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]
    
    log_with_context('info', 'Successfully retrieved users', count=len(users))
    return jsonify(users), 200

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Endpoint to create order with error handling and logging."""
    data = request.get_json() or {}
    log_with_context('info', 'Received request to create order', payload=data)
    
    if 'user_id' not in data or 'amount' not in data:
        log_with_context('error', 'Validation failed for order creation', missing_fields=True)
        return jsonify({"error": "Missing required fields: user_id, amount"}), 400
        
    order = {
        "order_id": str(uuid.uuid4()),
        "user_id": data.get('user_id'),
        "amount": data.get('amount')
    }
    
    log_with_context('info', 'Order created successfully', order_id=order['order_id'])
    return jsonify(order), 201

@app.route('/api/orders/full', methods=['POST'])
def create_full_order():
    """Create order with downstream inventory check (correlation ID propagation)."""
    data = request.get_json() or {}
    product_id = data.get('product_id', 'unknown-prod')
    
    log_with_context('info', 'Starting full order processing workflow', product_id=product_id)
    
    # Propagate correlation ID to downstream Service B
    headers = {
        'X-Correlation-ID': getattr(g, 'correlation_id', 'N/A'),
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            'http://localhost:5001/api/inventory/check',
            json={'product_id': product_id},
            headers=headers,
            timeout=3
        )
        inventory_res = response.json()
        log_with_context('info', 'Received response from inventory service', inventory_status=inventory_res)
    except Exception as e:
        log_with_context('error', 'Failed to communicate with inventory service', error=str(e))
        return jsonify({"error": "Inventory service communication failure"}), 502
        
    order = {
        "order_id": str(uuid.uuid4()),
        "product_id": product_id,
        "inventory_checked": True,
        "status": "confirmed"
    }
    
    log_with_context('info', 'Full order completed and confirmed', order_id=order['order_id'])
    return jsonify(order), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
