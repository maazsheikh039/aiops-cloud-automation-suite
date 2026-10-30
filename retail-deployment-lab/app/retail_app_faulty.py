from flask import Flask, jsonify
import time
import os

app = Flask(__name__)

app_state = {
    'version': os.getenv('APP_VERSION', '2.0.0'),
    'start_time': time.time(),
    'healthy': False,  # Intentionally unhealthy
    'ready': False
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
    return jsonify({'status': 'unhealthy'}), 503

@app.route('/ready')
def ready():
    return jsonify({'status': 'not ready'}), 503

@app.route('/products')
def products():
    return jsonify({'error': 'Service unavailable'}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
