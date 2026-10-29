# Containerized Microservice Architecture (Flask API, Worker, & Redis)

## Objectives
- Build production-ready, lightweight Dockerfiles (`python:3.11-slim`) for Python microservices.
- Orchestrate multi-container deployments using Docker bridge networks and Docker Compose.
- Implement an asynchronous task queue pattern connecting a REST API to a background worker via Redis.
- Maintain shared configuration modules across independent service build contexts.

## Tools Used
- **Docker & Docker Compose**: Container runtime, image building, and multi-service orchestration.
- **Python / Flask**: Lightweight REST API web server handling client requests.
- **Redis**: In-memory data store acting as the message broker and result cache.

## Key Skills Demonstrated
- **Containerization Best Practices**: Utilizing slim base images, explicit workdirs, and cached dependency installations.
- **Microservices Networking**: Establishing isolated bridge networks for secure inter-container communication.
- **Asynchronous Processing**: Decoupling synchronous HTTP endpoints from heavy background worker jobs.
- **Environment Configuration**: Injecting runtime variables dynamically via environment mapping.

## Troubleshooting Log
- **Issue**: Python failing to import shared modules across different service directories inside the container.
  - **Resolution**: Added explicit context mapping in Dockerfiles and appended `/app` to `sys.path` within service entrypoints.
- **Issue**: Worker container starting before Redis was ready to accept connections.
  - **Resolution**: Configured `depends_on` inside Docker Compose to manage service startup sequencing.
