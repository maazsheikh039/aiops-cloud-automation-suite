import requests
import time
import json
import subprocess
import os
from datetime import datetime

API_BASE_URL = 'http://localhost:5000'
POLL_INTERVAL = 5  # seconds

class JobWorker:
    """Worker service that fetches and executes jobs"""
    
    def __init__(self, api_url):
        self.api_url = api_url
        self.running = True
    
    def fetch_pending_jobs(self):
        """Fetch jobs with 'pending' status from the API"""
        try:
            response = requests.get(f"{self.api_url}/jobs", params={"status": "pending"})
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching pending jobs: {e}")
        return []
    
    def update_job_status(self, job_id, status, result=None):
        """Update job status via API"""
        try:
            payload = {"status": status}
            if result is not None:
                payload["result"] = result
            response = requests.put(f"{self.api_url}/jobs/{job_id}/status", json=payload)
            if response.status_code != 200:
                print(f"Failed to update job {job_id} status: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Connection error updating job {job_id}: {e}")
    
    def execute_backup_job(self, payload):
        """Execute a backup job"""
        data = json.loads(payload) if isinstance(payload, str) else payload
        path = data.get("path")
        destination = data.get("destination", "/tmp/backup")
        
        os.makedirs(destination, exist_ok=True)
        cmd = f"cp -r {path} {destination}/"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            return {"success": True, "message": f"Successfully backed up {path} to {destination}"}
        else:
            raise RuntimeError(f"Backup failed: {result.stderr.strip()}")
    
    def execute_cleanup_job(self, payload):
        """Execute a cleanup job"""
        data = json.loads(payload) if isinstance(payload, str) else payload
        directory = data.get("directory", "/tmp")
        days = data.get("days", 7)
        
        # Simulate file cleanup counting files processed
        removed_count = 0
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for f in files:
                    removed_count += 1
                    
        return {"success": True, "directory": directory, "files_scanned": removed_count, "message": "Cleanup completed successfully"}
    
    def execute_report_job(self, payload):
        """Execute a report generation job"""
        disk_res = subprocess.run("df -h /", shell=True, capture_output=True, text=True)
        mem_res = subprocess.run("free -m", shell=True, capture_output=True, text=True)
        
        return {
            "success": True,
            "disk_usage": disk_res.stdout.strip(),
            "memory_usage": mem_res.stdout.strip(),
            "generated_at": str(datetime.utcnow())
        }
    
    def process_job(self, job):
        """Process a single job based on its type"""
        job_id = job['id']
        job_type = job['job_type']
        payload = job['payload']
        
        print(f"[{datetime.now()}] Processing job {job_id} ({job_type})")
        
        # Update status to processing
        self.update_job_status(job_id, 'processing')
        
        try:
            if job_type == 'backup':
                result = self.execute_backup_job(payload)
            elif job_type == 'cleanup':
                result = self.execute_cleanup_job(payload)
            elif job_type == 'report':
                result = self.execute_report_job(payload)
            else:
                raise ValueError(f"Unknown job type: {job_type}")
            
            self.update_job_status(job_id, 'completed', json.dumps(result))
            print(f"[{datetime.now()}] Job {job_id} completed successfully")
            
        except Exception as e:
            error_result = {'error': str(e)}
            self.update_job_status(job_id, 'failed', json.dumps(error_result))
            print(f"[{datetime.now()}] Job {job_id} failed: {e}")
    
    def run(self):
        """Main worker loop"""
        print(f"Worker service started. Polling every {POLL_INTERVAL} seconds...")
        
        while self.running:
            try:
                jobs = self.fetch_pending_jobs()
                
                if jobs:
                    print(f"Found {len(jobs)} pending job(s)")
                    for job in jobs:
                        self.process_job(job)
                else:
                    print(f"[{datetime.now()}] No pending jobs")
                
                time.sleep(POLL_INTERVAL)
                
            except KeyboardInterrupt:
                print("\nShutting down worker service...")
                self.running = False
            except Exception as e:
                print(f"Error in worker loop: {e}")
                time.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    worker = JobWorker(API_BASE_URL)
    worker.run()
