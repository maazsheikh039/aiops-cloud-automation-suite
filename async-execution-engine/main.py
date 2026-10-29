import asyncio
from execution_engine import AsyncExecutionEngine
from task_model import Task
from sample_tasks import fetch_url, compute_intensive_task, process_file
import uuid

async def main():
    """Main application demonstrating the async execution engine."""
    engine = AsyncExecutionEngine(max_workers=3)
    await engine.start()
    
    print("Async Execution Engine Started")
    print("-" * 50)
    
    # Create sample test file
    await process_file("test_input.txt", "write")
    
    # Submit multiple tasks
    task_ids = []
    
    t1 = Task(task_id=str(uuid.uuid4()), func=compute_intensive_task, args=(2,))
    t2 = Task(task_id=str(uuid.uuid4()), func=process_file, args=("test_input.txt", "read"))
    t3 = Task(task_id=str(uuid.uuid4()), func=fetch_url, args=("https://httpbin.org/delay/1",))
    
    for t in [t1, t2, t3]:
        tid = await engine.submit_task(t)
        task_ids.append(tid)
        print(f"Submitted task: {tid} ({t.func.__name__})")
        
    # Wait for tasks to complete
    await asyncio.sleep(4)
    
    print("\nTask Results:")
    print("-" * 50)
    for tid in task_ids:
        status = engine.get_task_status(tid)
        print(f"Task {tid[:8]}... -> Status: {status['status'].upper()} | Result: {status['result']}")
        
    print("\nEngine Statistics:")
    print("-" * 50)
    print(engine.get_statistics())
    
    await engine.stop()
    print("\nEngine stopped")

if __name__ == "__main__":
    asyncio.run(main())
