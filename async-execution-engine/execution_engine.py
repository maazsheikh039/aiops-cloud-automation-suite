import asyncio
from typing import List, Dict, Any
from task_model import Task, TaskStatus
import time

class AsyncExecutionEngine:
    """
    Manages asynchronous task execution with concurrency control.
    """
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.task_queue = asyncio.Queue()
        self.tasks: Dict[str, Task] = {}
        self.workers: List[asyncio.Task] = []
        self.running = False
    
    async def submit_task(self, task: Task) -> str:
        """Submit a task for execution."""
        self.tasks[task.task_id] = task
        await self.task_queue.put(task)
        return task.task_id
    
    async def _worker(self, worker_id: int):
        """Worker coroutine that processes tasks from the queue."""
        print(f"Worker {worker_id} started")
        
        while self.running:
            try:
                # Get task from queue with timeout to allow graceful shutdown
                task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                
                task.status = TaskStatus.RUNNING
                try:
                    if asyncio.iscoroutinefunction(task.func):
                        res = await task.func(*task.args, **task.kwargs)
                    else:
                        res = task.func(*task.args, **task.kwargs)
                    
                    task.result = res
                    task.status = TaskStatus.COMPLETED
                except Exception as e:
                    task.error = str(e)
                    task.status = TaskStatus.FAILED
                finally:
                    task.completed_at = time.time()
                    self.task_queue.task_done()
                    
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Worker {worker_id} error: {e}")
        
        print(f"Worker {worker_id} stopped")
    
    async def start(self):
        """Start the execution engine and worker pool."""
        self.running = True
        self.workers = [
            asyncio.create_task(self._worker(i)) 
            for i in range(self.max_workers)
        ]
    
    async def stop(self):
        """Stop the execution engine gracefully."""
        self.running = False
        # Wait for queue to drain
        await self.task_queue.join()
        
        # Cancel workers
        for worker in self.workers:
            worker.cancel()
            
        await asyncio.gather(*self.workers, return_exceptions=True)
        self.workers.clear()
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get the status of a specific task."""
        task = self.tasks.get(task_id)
        if not task:
            return {"error": "Task not found"}
            
        return {
            "task_id": task.task_id,
            "status": task.status.value,
            "result": task.result,
            "error": task.error,
            "created_at": task.created_at,
            "completed_at": task.completed_at,
            "duration": (task.completed_at - task.created_at) if task.completed_at else None
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get execution statistics."""
        stats = {
            "total": len(self.tasks),
            "pending": 0,
            "running": 0,
            "completed": 0,
            "failed": 0
        }
        
        durations = []
        for task in self.tasks.values():
            stats[task.status.value] += 1
            if task.completed_at and task.created_at:
                durations.append(task.completed_at - task.created_at)
                
        stats["avg_execution_time"] = (sum(durations) / len(durations)) if durations else 0
        return stats

    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending or running task."""
        task = self.tasks.get(task_id)
        if not task:
            return False

        if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            return False

        task.status = TaskStatus.FAILED
        task.error = "Task cancelled by operator"
        task.completed_at = time.time()
        return True

    
