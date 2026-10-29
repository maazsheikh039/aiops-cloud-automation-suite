import asyncio
from execution_engine import AsyncExecutionEngine
from task_model import Task
from sample_tasks import compute_intensive_task
from monitor import EngineMonitor
import uuid

async def stress_test():
    """Stress test the execution engine with many tasks."""
    engine = AsyncExecutionEngine(max_workers=5)
    await engine.start()
    
    monitor = EngineMonitor(engine)
    monitor_task = asyncio.create_task(monitor.display_stats(interval=0.5))
    
    print("Submitting 20 stress tasks...")
    tasks = [
        Task(task_id=str(uuid.uuid4()), func=compute_intensive_task, args=(1,))
        for _ in range(20)
    ]
    
    for t in tasks:
        await engine.submit_task(t)
        
    await asyncio.sleep(6)
    monitor.stop()
    await monitor_task
    
    print("\nFinal Engine Statistics:")
    print(engine.get_statistics())
    await engine.stop()

if __name__ == "__main__":
    asyncio.run(stress_test())
