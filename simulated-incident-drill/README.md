# Simulated Incident Response Drill & Chaos Engineering Framework

## Objectives
- Simulate realistic production incidents (disk space exhaustion, service crashes with bad config, and CPU spikes).
- Implement structured incident response runbooks for rapid detection, diagnosis, and mitigation.
- Build a Python-based programmatic incident logger (`incident_logger.py`) to record actions and timelines.
- Automate drill execution and audit log capture via end-to-end shell scripts.

## Tools Used
- **Bash & Python**: Incident triggers, automated drill runners, and JSON log management.
- **Nginx & PostgreSQL**: Core application services subject to simulated failure scenarios.
- **Stress-ng & Sysstat**: CPU load injection and system resource monitoring tools.

## Key Skills Demonstrated
- **Chaos Engineering**: Proactively injecting failures into test systems to validate resilience and monitoring.
- **Runbook Adherence**: Following step-by-step operational guides to resolve incidents systematically.
- **Post-Incident Review**: Capturing structured timelines, root causes, and lessons learned for continuous improvement.
