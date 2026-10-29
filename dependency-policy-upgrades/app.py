"""
Sample application with dependencies
"""
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route('/fetch')
def fetch_data():
    """Fetch external data with basic error handling"""
    try:
        response = requests.get('https://api.github.com', timeout=5)
        return jsonify({"status_code": response.status_code})
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
