import asyncio
import aiohttp
import aiofiles

async def fetch_url(url: str) -> dict:
    """Fetch content from a URL asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()
            return {
                "status": response.status,
                "content_length": len(content)
            }

async def process_file(filename: str, operation: str) -> dict:
    """Process a file asynchronously."""
    if operation == "write":
        async with aiofiles.open(filename, mode='w') as f:
            await f.write("Async file operation test data.")
        return {"operation": "write", "status": "success", "file": filename}
    elif operation == "read":
        async with aiofiles.open(filename, mode='r') as f:
            content = await f.read()
        return {"operation": "read", "status": "success", "content_length": len(content)}
    else:
        raise ValueError(f"Unknown operation: {operation}")

async def compute_intensive_task(n: int) -> int:
    """Simulate a compute-intensive task."""
    await asyncio.sleep(n)  # Simulating heavy computation work
    return n * n
