from flask import Flask, jsonify, request
import redis
import json
import sys
import uuid
sys.path.append('/app')
from shared.config import Config

app = Flask(__name__)

def get_redis_client():
    return redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/task', methods=['POST'])
def create_task():
    '''
    Accept task data and queue it in Redis.
    Expected JSON: {"task_type": "process", "data": {...}}
    '''
    data = request.get_json() or {}
    task_type = data.get('task_type', 'default')
    task_payload = data.get('data', {})
    
    task_id = str(uuid.uuid4())
    task_item = {
        "task_id": task_id,
        "task_type": task_type,
        "data": task_payload
    }
    
    r = get_redis_client()
    r.rpush('task_queue', json.dumps(task_item))
    
    return jsonify({"status": "queued", "task_id": task_id}), 201

@app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):
    '''
    Retrieve task result from Redis.
    '''
    r = get_redis_client()
    result = r.get(f'result:{task_id}')
    
    if not result:
        return jsonify({"error": "Task result not found or still processing"}), 404
        
    return jsonify({"task_id": task_id, "result": json.loads(result)}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.API_PORT)
