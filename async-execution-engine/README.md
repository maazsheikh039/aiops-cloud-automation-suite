# Asynchronous Execution Engine & Concurrency Worker Pool

## Objectives
- Build a scalable asynchronous task execution engine leveraging Python's `asyncio` and worker pool patterns.
- Implement non-blocking task queues with status lifecycle management (`pending`, `running`, `completed`, `failed`).
- Integrate asynchronous I/O handlers using `aiohttp` and `aiofiles` for high-throughput operations.
- Provide real-time operational monitoring dashboards and performance statistics tracking.

## Tools Used
- **Python `asyncio`**: Event loop concurrency, coroutine workers, and asynchronous queue management.
- **`aiohttp` & `aiofiles`**: Asynchronous HTTP client sessions and non-blocking file read/write operations.
- **Dataclasses & Enums**: Strict type modeling for task specifications and state machine tracking.

## Key Skills Demonstrated
- **Concurrent System Design**: Decoupling task submission from execution using bounded worker pools to prevent resource exhaustion.
- **Non-Blocking I/O Architecture**: Handling high-concurrency network requests and disk operations without thread blocking.
- **Observability & Telemetry**: Aggregating execution times, success ratios, and live status states.
- **Fault Tolerance**: Graceful error catching and task cancellation support within asynchronous worker coroutines.

## Troubleshooting Log
- **Issue**: Event loop warnings when cancelling workers during active task execution.
  - **Resolution**: Implemented graceful queue joining (`await self.task_queue.join()`) and proper coroutine cancellation handling with `asyncio.gather(..., return_exceptions=True)`.
- **Issue**: File I/O blocking the main async loop.
  - **Resolution**: Replaced standard synchronous file handling with `aiofiles` to ensure all disk operations execute asynchronously.
