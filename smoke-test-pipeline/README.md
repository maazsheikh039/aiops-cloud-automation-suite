# Automated Smoke Test & Post-Deployment Validation Pipeline

## Objectives
- Build an end-to-end automated deployment pipeline incorporating pre-check validation, server deployment, and post-deployment smoke tests.
- Verify core REST endpoints (`/health`, `/api/data`, `/api/status`) and measure HTTP response latency thresholds.
- Generate structured test reports with timestamps and log notifications for success or failure states.
- Enforce strict pipeline exit codes (`0` for success, `1` for failure) for CI/CD quality gate integration.

## Tools Used
- **Bash Scripting**: Orchestrating deployment stages, background node processes, and log handling.
- **cURL & `jq`**: HTTP request generation and response status code validation.
- **Node.js**: Lightweight HTTP web application server simulating microservice endpoints.

## Key Skills Demonstrated
- **CI/CD Quality Gates**: Preventing broken code or failed deployments from passing unnoticed into production.
- **Observability & Alerting**: Generating structured test summaries and automated notification logs.
- **Latency Monitoring**: Checking application response times against SLA thresholds (under 2 seconds).
