import asyncio
from execution_engine import AsyncExecutionEngine
import os

class EngineMonitor:
    """Monitor and display engine statistics."""
    
    def __init__(self, engine: AsyncExecutionEngine):
        self.engine = engine
        self.monitoring = False
    
    async def display_stats(self, interval: int = 1):
        """Display engine statistics periodically."""
        self.monitoring = True
        
        while self.monitoring:
            os.system('clear' if os.name == 'posix' else 'cls')
            stats = self.engine.get_statistics()
            
            print("=" * 40)
            print(" ASYNC ENGINE MONITORING DASHBOARD")
            print("=" * 40)
            print(f" Total Tasks : {stats['total']}")
            print(f" Pending     : {stats['pending']}")
            print(f" Running     : {stats['running']}")
            print(f" Completed   : {stats['completed']}")
            print(f" Failed      : {stats['failed']}")
            print(f" Avg Time    : {stats['avg_execution_time']:.4f}s")
            print("=" * 40)
            
            await asyncio.sleep(interval)
    
    def stop(self):
        """Stop monitoring."""
        self.monitoring = False
