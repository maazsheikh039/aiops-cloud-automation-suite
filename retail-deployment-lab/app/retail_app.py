from flask import Flask, jsonify
import time
import os

app = Flask(__name__)

# Application state
app_state = {
    'version': os.getenv('APP_VERSION', '1.0.0'),
    'start_time': time.time(),
    'healthy': True,
    'ready': True
}

@app.route('/')
def home():
    return jsonify({
        'service': 'Retail Pack API',
        'version': app_state['version'],
        'status': 'running'
    })

@app.route('/health')
def health():
    """Health check endpoint for deployment gates."""
    if not app_state['healthy']:
        return jsonify({'status': 'unhealthy'}), 503
    
    return jsonify({
        'status': 'healthy',
        'version': app_state['version']
    }), 200

@app.route('/ready')
def ready():
    """Readiness check endpoint."""
    uptime = time.time() - app_state['start_time']
    
    # Enforce a 2-second warmup period
    if uptime < 2.0:
        return jsonify({'status': 'warming up', 'uptime': uptime}), 503
    
    if not app_state['ready']:
        return jsonify({'status': 'not ready'}), 503
    
    return jsonify({
        'status': 'ready',
        'uptime': uptime
    }), 200

@app.route('/products')
def products():
    return jsonify({
        'products': [
            {'id': 1, 'name': 'Laptop', 'price': 999.99},
            {'id': 2, 'name': 'Mouse', 'price': 29.99}
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
