from flask import Flask, request, jsonify
import redis
import json
import uuid
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from policies.policy_engine import PolicyEngine
from workers.task_worker import execute_automation_task

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
policy_engine = PolicyEngine()

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create new automation task."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
        
    is_valid, msg = policy_engine.validate_task(data)
    if not is_valid:
        return jsonify({"error": msg}), 400
        
    task_type = data.get('task_type')
    parameters = data.get('parameters', {})
    priority = data.get('priority', 'medium')
    
    task_id = f"{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
    
    task_meta = {
        'task_id': task_id,
        'task_type': task_type,
        'parameters': parameters,
        'priority': priority,
        'status': 'QUEUED',
        'created_at': datetime.now().isoformat()
    }
    
    # Store in Redis
    r.setex(f"task:{task_id}", 3600, json.dumps(task_meta))
    
    # Queue task to Celery
    execute_automation_task.apply_async(args=[task_id, task_type, parameters], task_id=task_id)
    
    return jsonify({"message": "Task created successfully", "task_id": task_id, "status": "QUEUED"}), 201

@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id: str):
    """Retrieve task status and results."""
    raw = r.get(f"task:{task_id}")
    if not raw:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(json.loads(raw)), 200

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    """List all tasks with optional filtering."""
    status_filter = request.args.get('status')
    type_filter = request.args.get('type')
    
    keys = r.keys("task:*")
    tasks = []
    for k in keys:
        raw = r.get(k)
        if raw:
            try:
                t = json.loads(raw)
                if status_filter and t.get('status') != status_filter.upper():
                    continue
                if type_filter and t.get('task_type') != type_filter:
                    continue
                tasks.append(t)
            except Exception:
                continue
                
    return jsonify({"count": len(tasks), "tasks": tasks}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
