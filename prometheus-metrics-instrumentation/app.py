from flask import Flask, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
import time
import random

app = Flask(__name__)

# Counter metric for total HTTP requests
http_requests = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

# Histogram metric for request duration
request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Gauge metric for active connections
active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

# Gauge metric for system health score (0-100)
health_score = Gauge(
    'system_health_score',
    'Current system health score'
)

@app.route('/')
def home():
    active_connections.inc()
    start_time = time.time()
    
    time.sleep(random.uniform(0.1, 0.5))
    
    duration = time.time() - start_time
    request_duration.labels(method='GET', endpoint='/').observe(duration)
    http_requests.labels(method='GET', endpoint='/', status_code='200').inc()
    
    active_connections.dec()
    return "Hello from Instrumented App!"

@app.route('/api/data')
def api_data():
    active_connections.inc()
    start_time = time.time()
    
    time.sleep(random.uniform(0.2, 0.8))
    
    duration = time.time() - start_time
    request_duration.labels(method='GET', endpoint='/api/data').observe(duration)
    http_requests.labels(method='GET', endpoint='/api/data', status_code='200').inc()
    
    active_connections.dec()
    return {"status": "success", "data": [1, 2, 3, 4, 5]}

@app.route('/health')
def health():
    score = random.randint(50, 100)
    health_score.set(score)
    return {"health": "ok", "score": score}

@app.route('/metrics')
def metrics():
    return Response(generate_latest(REGISTRY), mimetype='text/plain')

if __name__ == '__main__':
    health_score.set(100)
    app.run(host='0.0.0.0', port=8000)
