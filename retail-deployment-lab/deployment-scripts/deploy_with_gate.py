#!/usr/bin/env python3
import subprocess
import requests
import time
import yaml
import sys
import os

class DeploymentGate:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)['deployment']
        self.app_name = self.config['app_name']
        self.port = self.config['port']
        self.current_container = None
        self.previous_container = None
        
    def get_running_container(self):
        """Get currently running container ID."""
        try:
            result = subprocess.run(
                ['docker', 'ps', '-q', '-f', f'name={self.app_name}'],
                capture_output=True, text=True
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"Error getting container: {e}")
            return None
    
    def stop_container(self, container_id):
        """Stop a container."""
        if container_id:
            subprocess.run(['docker', 'stop', container_id], capture_output=True)
            subprocess.run(['docker', 'rm', container_id], capture_output=True)
    
    def start_new_version(self, version):
        """Start new version of the application."""
        print(f"Starting new version: {version}")
        
        self.previous_container = self.get_running_container()
        
        if self.previous_container:
            print(f"Stopping previous container: {self.previous_container}")
            # Stop but do not remove immediately if keeping previous for rollback
            subprocess.run(['docker', 'stop', self.previous_container], capture_output=True)
        
        try:
            result = subprocess.run([
                'docker', 'run', '-d',
                '--name', f'{self.app_name}',
                '-p', f'{self.port}:{self.port}',
                '-e', f'APP_VERSION={version}',
                f'{self.app_name}:{version}'
            ], capture_output=True, text=True)
            
            self.current_container = result.stdout.strip()
            print(f"Started container: {self.current_container}")
            return True
        except Exception as e:
            print(f"Failed to start container: {e}")
            return False
    
    def health_check(self):
        """Perform health check on deployed application with retries."""
        config = self.config['health_check']
        endpoint = f"http://localhost:{self.port}{config['endpoint']}"
        
        print(f"Performing health check on {endpoint}")
        
        for attempt in range(config['retries']):
            try:
                response = requests.get(endpoint, timeout=config['timeout'])
                if response.status_code == 200:
                    print(f"Health check passed: {response.json()}")
                    return True
                else:
                    print(f"Health check failed with status: {response.status_code}")
            except Exception as e:
                print(f"Health check attempt {attempt + 1} failed: {e}")
            
            time.sleep(config['interval'])
        
        return False
    
    def readiness_check(self):
        """Perform readiness check with retries."""
        config = self.config['readiness_check']
        endpoint = f"http://localhost:{self.port}{config['endpoint']}"
        
        print(f"Performing readiness check on {endpoint}")
        
        for attempt in range(config['retries']):
            try:
                response = requests.get(endpoint, timeout=config['timeout'])
                if response.status_code == 200:
                    print(f"Readiness check passed: {response.json()}")
                    return True
                else:
                    print(f"Readiness check returned status: {response.status_code}")
            except Exception as e:
                print(f"Readiness attempt {attempt + 1} failed: {e}")
            
            time.sleep(config['interval'])
        
        return False
    
    def rollback(self):
        """Rollback to previous version."""
        print("INITIATING ROLLBACK...")
        
        if not self.previous_container:
            print("No previous version to rollback to!")
            return False
        
        if self.current_container:
            print(f"Stopping failed container: {self.current_container}")
            self.stop_container(self.current_container)
        
        try:
            print(f"Restarting previous container: {self.previous_container}")
            subprocess.run(['docker', 'start', self.previous_container], capture_output=True)
            
            time.sleep(3)
            if self.health_check():
                print("ROLLBACK SUCCESSFUL")
                return True
            else:
                print("ROLLBACK FAILED - Manual intervention required")
                return False
        except Exception as e:
            print(f"Rollback error: {e}")
            return False
    
    def deploy(self, version):
        """Main deployment function with gates."""
        print(f"\n{'='*50}")
        print(f"DEPLOYMENT GATE: Starting deployment of version {version}")
        print(f"{'='*50}\n")
        
        if not self.start_new_version(version):
            print("Failed to start new version")
            return False
        
        time.sleep(2)
        
        print("\nGATE 1: Health Check")
        if not self.health_check():
            print("GATE FAILED: Health check did not pass")
            if self.config['rollback']['on_failure']:
                self.rollback()
            return False
        
        print("\nGATE 2: Readiness Check")
        if not self.readiness_check():
            print("GATE FAILED: Readiness check did not pass")
            if self.config['rollback']['on_failure']:
                self.rollback()
            return False
        
        print("\n" + "="*50)
        print("DEPLOYMENT SUCCESSFUL - All gates passed")
        print("="*50)
        
        if self.previous_container and not self.config['rollback']['keep_previous']:
            subprocess.run(['docker', 'rm', self.previous_container], capture_output=True)
        
        return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 deploy_with_gate.py <version>")
        sys.exit(1)
    
    version = sys.argv[1]
    gate = DeploymentGate('config/deployment.yaml')
    success = gate.deploy(version)
    sys.exit(0 if success else 1)
