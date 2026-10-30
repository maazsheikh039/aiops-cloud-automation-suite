#!/usr/bin/env python3
"""
Simple webhook server to receive alerts
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class AlertHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle incoming alert POST requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        try:
            alert_data = json.loads(body)
            print(f"Received Webhook Alert: {json.dumps(alert_data, indent=2)}")
        except json.JSONDecodeError:
            print(f"Received Raw Webhook Alert: {body}")
            
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "received"}')

if __name__ == "__main__":
    server = HTTPServer(('localhost', 8080), AlertHandler)
    print("Alert webhook listening on port 8080...")
    server.serve_forever()
