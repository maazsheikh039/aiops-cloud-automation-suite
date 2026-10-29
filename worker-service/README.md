# Asynchronous Job Queue and Worker Service Architecture

## Objectives
- Implement a decoupled worker service pattern for asynchronous task automation and background execution.
- Build a persistent relational job queue backend with SQLite and Flask REST APIs.
- Manage full job lifecycles (`pending` -> `processing` -> `completed`/`failed`) with robust error handling.
- Execute automated system operations (backups, cleanup routines, telemetry reports) safely using Python subprocesses.

## Tools Used
- **Python / Flask**: RESTful API server handling job creation, status updates, and queue queries.
- **SQLite**: Lightweight relational database backend serving as the persistent task queue.
- **Requests Library**: HTTP client facilitating communication between worker nodes and API orchestrators.
- **Subprocess & OS Modules**: Executing administrative shell tasks and directory manipulation.

## Key Skills Demonstrated
- **Distributed Systems Patterns**: Designing polling-based worker architectures to decouple heavy workloads from web APIs.
- **State Machine Management**: Tracking job execution phases and storing structured JSON results/error logs.
- **Process Automation**: Automating routine infrastructure tasks like system backups and resource cleanup.
- **Fault Tolerance**: Catching runtime exceptions during job execution and transitioning tasks to `failed` states gracefully.

## Troubleshooting Log
- **Issue**: SQLite database locking during concurrent API writes and worker status updates.
  - **Resolution**: Enabled SQLite connection isolation and proper cursor management within request contexts to prevent resource contention.
- **Issue**: Worker failing to execute system commands due to relative path or permission errors.
  - **Resolution**: Configured absolute paths and targeted safe staging directories (`/tmp`) for file copy and backup testing.
