# Retail Deployment Gate and Rollback Trigger

## Objectives
- Implement automated deployment safety gates protecting customer-facing production microservices.
- Configure health and readiness verification endpoints with retry policies and timeouts.
- Create automated rollback mechanisms to immediately restore previous stable versions upon failure.
- Minimize Mean Time To Recovery (MTTR) for e-commerce and retail environments.

## Tools Used
- Python 3, Flask, Requests, PyYAML
- Docker Container Engine
- Bash & Git

## Key Skills Demonstrated
- **CI/CD Safety Gates:** Enforcing strict programmatic health checks before accepting live traffic.
- **Automated Rollback Engineering:** Designing self-healing deployment pipelines that revert broken updates instantly.
- **Microservice Lifecycle Management:** Orchestrating container replacement and state preservation.

## Troubleshooting Log
- **Container Port Bindings:** Handled active port conflicts on port 5000 during rolling updates by stopping and releasing previous container bindings before starting new instances.
