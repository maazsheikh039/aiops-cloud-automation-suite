# Queryable Job History API with Test Suite

## Objectives
- Build a production-grade REST API for tracking and querying automated job execution histories.
- Implement advanced dynamic query filtering by status, environment, user, and execution date ranges.
- Provide statistical aggregation endpoints for monitoring platform health and job success ratios.
- Maintain rigorous test coverage using `pytest` and Flask test clients.

## Tools Used
- **Python / Flask**: Lightweight WSGI application framework and routing blueprint architecture.
- **SQLAlchemy ORM**: Relational database modeling and transactional state management.
- **Pytest & Pytest-Flask**: Automated integration testing framework with fixture isolation and code coverage metrics.
- **SQLite**: Local persistent storage for job run logs and audit trails.

## Key Skills Demonstrated
- **RESTful API Design**: Designing standard HTTP CRUD endpoints with robust error handling and query parameter validation.
- **Database Querying & Optimization**: Constructing dynamic ORM filter chains and group-by statistical aggregations.
- **Test-Driven Reliability**: Writing isolated test fixtures and comprehensive validation suites ensuring 80%+ code coverage.
- **DevOps Observability**: Establishing audit trails and execution tracking for automated workflows and background tasks.

## Troubleshooting Log
- **Issue**: SQLite database locking during concurrent test execution.
  - **Resolution**: Configured isolated test configuration (`TestConfig`) using separate test databases (`test_job_history.db`) and proper session teardown fixtures in `pytest`.
- **Issue**: Datetime string parsing errors during updates and date filtering.
  - **Resolution**: Implemented explicit ISO format parsing and `YYYY-MM-DD` string conversions with fallback `400 Bad Request` validation handlers.
