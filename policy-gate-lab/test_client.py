#!/usr/bin/env python3
import requests
import json

class PolicyGateClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
    
    def switch_profile(self, profile_name: str) -> dict:
        resp = requests.post(f"{self.base_url}/switch-profile", json={"profile": profile_name})
        return resp.json()
    
    def enforce_request(self, request_data: dict) -> dict:
        resp = requests.post(f"{self.base_url}/enforce", json=request_data)
        return resp.json()
    
    def get_status(self) -> dict:
        resp = requests.get(f"{self.base_url}/status")
        return resp.json()

if __name__ == "__main__":
    client = PolicyGateClient()
    print("Status:", client.get_status())
