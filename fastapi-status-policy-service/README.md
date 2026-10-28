# FastAPI Status and Policy Service

A production-grade microservice built with FastAPI for automated system health monitoring, infrastructure telemetry, and centralized policy enforcement.

## Objectives
- Expose RESTful endpoints for health checks, system resource metrics (`psutil`), and policy metadata.
- Implement robust request validation using Pydantic data models.
- Build custom policy evaluators for request sizing, HTTP method whitelisting, and in-memory rate limiting.
- Integrate custom middleware for real-time request/response logging and performance tracking.

## Tools Used
- **FastAPI** for high-performance asynchronous REST API development
- **Uvicorn** as the ASGI server
- **Pydantic** for typed data parsing and validation
- **Psutil** for cross-platform system telemetry
- **Linux Terminal** & Curl for testing

## Key Skills Demonstrated
- **Microservice Architecture:** Designing structured, modular FastAPI applications with clear separation of concerns (models, policies, config, main).
- **Security & Governance:** Enforcing automated compliance policies on incoming payloads at the application edge.
- **Observability:** Capturing telemetry and middleware request logs for audit trails.
