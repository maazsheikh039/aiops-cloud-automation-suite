# Incident Response Runbook: Cpu Usage Is At 95% And Application Is Slow

**Generated:** 2026-10-30T08:06:04.990306
**Hostname:** ip-172-31-10-135
**Scenario:** CPU usage is at 95% and application is slow

## System Information

- **OS:** Ubuntu 24.04.3 LTS
- **Kernel:** 6.14.0-1018-aws
- **Memory:** Checked via system collector

## Prerequisites

Root access / sudo privileges, SSH access, monitoring tool permissions.

## Procedure

Error connecting to Ollama service: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=120)

## Verification Steps

Run health checks, verify service responsiveness and CPU/disk metrics.

## Rollback Procedure

Revert configuration changes, restart affected services, or restore from snapshot if failure persists.

---
*Auto-generated runbook - Review before use in production*