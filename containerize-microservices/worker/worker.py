import redis
import json
import time
import sys
sys.path.append('/app')
from shared.config import Config

def get_redis_client():
    return redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

def process_task(task_data):
    '''
    Process the task based on task_type.
    Simulate work with time.sleep().
    '''
    task_type = task_data.get('task_type')
    payload = task_data.get('data')
    
    print(f"Processing task type: {task_type} with data: {payload}")
    time.sleep(3)  # Simulate heavy processing work
    
    return {"processed": True, "input": payload, "timestamp": time.time()}

def main():
    print("Worker starting...")
    r = get_redis_client()
    
    while True:
        try:
            # Block and pop task from 'task_queue' (BLPOP)
            queue_item = r.blpop('task_queue', timeout=0)
            if queue_item:
                _, task_json = queue_item
                task_data = json.loads(task_json)
                task_id = task_data.get('task_id')
                
                print(f"Executing task {task_id}...")
                result = process_task(task_data)
                
                # Store result in Redis
                r.set(f'result:{task_id}', json.dumps(result))
                print(f"Task {task_id} completed successfully.")
        except Exception as e:
            print(f"Worker error: {e}")
            time.sleep(2)

if __name__ == '__main__':
    main()
