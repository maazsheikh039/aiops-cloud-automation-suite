from flask import Flask, request, jsonify, g
import logging
from pythonjsonlogger import jsonlogger
import time

app = Flask(__name__)

def setup_logging():
    """Configure JSON logging for service B."""
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(correlation_id)s %(message)s'
    )
    log_handler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.handlers = []
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)
    
    return logger

logger = setup_logging()

@app.before_request
def before_request():
    """Extract correlation ID from incoming request headers."""
    g.correlation_id = request.headers.get('X-Correlation-ID', 'UNKNOWN-CORR-ID')

def log_with_context(level, message, **kwargs):
    """Log message with correlation ID for service B."""
    extra = {
        'correlation_id': getattr(g, 'correlation_id', 'N/A'),
        **kwargs
    }
    if level == 'info':
        logger.info(message, extra=extra)
    else:
        logger.error(message, extra=extra)

@app.route('/api/inventory/check', methods=['POST'])
def check_inventory():
    """Check inventory availability with contextual logging."""
    data = request.get_json() or {}
    product_id = data.get('product_id')
    
    log_with_context('info', 'Checking inventory availability for product', product_id=product_id)
    time.sleep(0.05)
    
    result = {
        "product_id": product_id,
        "available": True,
        "quantity": 50
    }
    
    log_with_context('info', 'Inventory check completed successfully', product_id=product_id, available=True)
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
