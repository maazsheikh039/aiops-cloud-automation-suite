# Automation Platform MVP

## Objectives
- Build an end-to-end task automation and orchestration platform comprising API, Worker, Policy Engine, and CLI components.
- Enforce strict declarative policy validation on inbound automation requests.
- Implement asynchronous task processing with retries using Celery and Redis.
- Provide a feature-rich Click CLI and Flask REST API for task submission and lifecycle monitoring.

## Tools Used
- Python 3, Flask, Celery, Redis, Click, PyYAML
- Bash & Git

## Key Skills Demonstrated
- **Distributed System Architecture:** Decoupling API request gateways from asynchronous worker queues using Redis message brokers.
- **Policy as Code:** Validating incoming payloads against declarative JSON/YAML business rules.
- **Developer Tooling:** Creating ergonomic CLI experiences with colored terminal outputs.

## Troubleshooting Log
- **Celery Application Module Path:** Configured explicit Redis broker URLs and app binding parameters in Celery workers to ensure seamless background task execution without import conflicts.
