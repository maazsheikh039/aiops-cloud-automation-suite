from celery import Celery
import time
import yaml
import os
import redis
import json
from datetime import datetime

# Load configuration for broker
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
else:
    config = {'redis': {'host': 'localhost', 'port': 6379, 'db': 0}}

redis_conf = config.get('redis', {})
broker_url = f"redis://{redis_conf.get('host', 'localhost')}:{redis_conf.get('port', 6379)}/{redis_conf.get('db', 0)}"

app = Celery('automation_platform', broker=broker_url, backend=broker_url)
r = redis.Redis(host=redis_conf.get('host', 'localhost'), port=redis_conf.get('port', 6379), db=redis_conf.get('db', 0))

@app.task(bind=True, max_retries=3)
def execute_automation_task(self, task_id: str, task_type: str, parameters: dict):
    """Execute automation task with retry logic."""
    print(f"[{datetime.now().isoformat()}] Starting task {task_id} of type '{task_type}'")
    
    # Update Redis status to running
    task_meta = {
        'task_id': task_id,
        'task_type': task_type,
        'parameters': parameters,
        'status': 'RUNNING',
        'updated_at': datetime.now().isoformat()
    }
    r.setex(f"task:{task_id}", 3600, json.dumps(task_meta))
    
    try:
        # Simulate execution based on task type
        if task_type == 'backup':
            path = parameters.get('path', '/default/path')
            dest = parameters.get('destination', '/default/dest')
            time.sleep(3) # Simulate workload
            result = f"Successfully backed up {path} to {dest}"
        elif task_type == 'deploy':
            service = parameters.get('service', 'unknown-service')
            version = parameters.get('version', 'latest')
            time.sleep(4)
            result = f"Successfully deployed service {service} version {version}"
        elif task_type == 'cleanup':
            target = parameters.get('target', 'temp')
            time.sleep(2)
            result = f"Successfully cleaned up target {target}"
        else:
            raise ValueError(f"Unsupported task type: {task_type}")
            
        task_meta['status'] = 'COMPLETED'
        task_meta['result'] = result
        task_meta['updated_at'] = datetime.now().isoformat()
        r.setex(f"task:{task_id}", 3600, json.dumps(task_meta))
        return task_meta
        
    except Exception as exc:
        print(f"Task {task_id} failed: {exc}")
        task_meta['status'] = 'FAILED'
        task_meta['error'] = str(exc)
        task_meta['updated_at'] = datetime.now().isoformat()
        r.setex(f"task:{task_id}", 3600, json.dumps(task_meta))
        raise self.retry(exc=exc, countdown=5)
