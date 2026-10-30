#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from policy_gate import PolicyGate
from config_manager import ConfigManager

class PolicyGateHandler(BaseHTTPRequestHandler):
    gate = None
    config_mgr = None
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._send_json_response({"error": "Invalid JSON"}, status=400)
            return
            
        if self.path == "/enforce":
            result = self.gate.enforce_policy(data)
            self._send_json_response(result)
            
        elif self.path == "/switch-profile":
            profile_name = data.get("profile")
            if not profile_name:
                self._send_json_response({"error": "Missing 'profile' field"}, status=400)
                return
                
            success = self.gate.switch_profile(profile_name)
            if success:
                self.config_mgr.set_active_profile(profile_name)
                self._send_json_response({"success": True, "active_profile": profile_name})
            else:
                self._send_json_response({"success": False, "error": f"Profile '{profile_name}' not found"}, status=404)
        else:
            self._send_json_response({"error": "Not Found"}, status=404)
    
    def do_GET(self):
        if self.path == "/status":
            status = self.gate.get_active_profile_info()
            self._send_json_response(status)
            
        elif self.path == "/profiles":
            profiles = self.config_mgr.list_available_profiles()
            self._send_json_response({"profiles": profiles})
        else:
            self._send_json_response({"error": "Not Found"}, status=404)
            
    def _send_json_response(self, data: dict, status: int = 200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

def run_server(port: int = 8080):
    gate = PolicyGate()
    config_mgr = ConfigManager()
    
    # Load all profiles
    profiles_dir = "config/profiles"
    if os.path.exists(profiles_dir):
        for f in os.listdir(profiles_dir):
            if f.endswith('.yaml'):
                gate.load_profile(os.path.join(profiles_dir, f))
                
    # Restore active profile if configured
    active = config_mgr.get_active_profile()
    if active:
        gate.switch_profile(active)
    elif gate.profiles:
        first_profile = list(gate.profiles.keys())[0]
        gate.switch_profile(first_profile)
        config_mgr.set_active_profile(first_profile)
        
    PolicyGateHandler.gate = gate
    PolicyGateHandler.config_mgr = config_mgr
    
    server = HTTPServer(('0.0.0.0', port), PolicyGateHandler)
    print(f"Policy Gate API Server running on port {port}...")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
