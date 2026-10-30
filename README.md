<div align="center">

<h1>AIOps Cloud Automation Suite</h1>

<p><strong>Cloud Operations · Automation · Platform Engineering</strong></p>

<p>A professional portfolio of engineering projects focused on cloud operations, platform automation, application reliability, governance, and observability.</p>

<p>
<a href="#project-directory"><img src="https://img.shields.io/badge/Explore-38%20Projects-2563EB?style=for-the-badge" alt="Explore 38 Projects"></a>
<a href="#technology-overview"><img src="https://img.shields.io/badge/Technology-Overview-475569?style=for-the-badge" alt="Technology Overview"></a>
<a href="#getting-started"><img src="https://img.shields.io/badge/Getting-Started-0F766E?style=for-the-badge" alt="Getting Started"></a>
</p>

<table align="center">
<tr>
<td align="center"><strong>38</strong><br>Projects</td>
<td align="center"><strong>5</strong><br>Engineering Areas</td>
<td align="center"><strong>Independent</strong><br>Project Setups</td>
</tr>
</table>

<p><a href="#automation-and-workflow-engineering">Automation</a> · <a href="#apis-applications-and-data">APIs &amp; Services</a> · <a href="#configuration-security-and-governance">Governance</a> · <a href="#observability-and-incident-response">Observability</a> · <a href="#reliability-delivery-and-engineering-practices">Reliability &amp; Delivery</a></p>

</div>

---

## Project Directory

### Automation and Workflow Engineering

| Project | Description |
|---|---|
| [Asynchronous Execution Engine](async-execution-engine/) | Python asyncio worker pool for queued tasks, lifecycle tracking, cancellation, and execution statistics. |
| [Automation Platform](automation-platform/) | Flask API, Celery workers, Redis queue, policy validation, and Click command-line interface. |
| [AI-Assisted Runbook Generator](ai-runbook-generator/) | Collects Linux system information and uses a local Ollama model to generate operational runbook documents. |
| [AI Test Suggestion Pipeline](ai-test-pipeline/) | Analyzes Git changes and Python syntax trees to produce prioritized test recommendations. |
| [CI Failure Triage Assistant](ci-triage-assistant/) | Applies configurable patterns to CI logs and extracts error context for investigation. |
| [Dependency-Aware Pipeline Runner](pipeline-runner/) | Executes YAML-defined jobs according to dependencies and reports cycle or failure conditions. |
| [Worker Service](worker-service/) | Flask job API and SQLite-backed queue for background operational tasks. |
| [Opsctl CLI](opsctl-core/) | Modular command-line interface for operational status, deployment, and configuration tasks. |
| [Smoke Test Pipeline](smoke-test-pipeline/) | Shell-based deployment flow with health and API endpoint checks for a Node.js service. |

### APIs, Applications, and Data

| Project | Description |
|---|---|
| [FastAPI Status and Policy Service](fastapi-status-policy-service/) | Health and system metrics endpoints with request validation, policy checks, and request logging. |
| [Job History API](job-history-api/) | Flask and SQLAlchemy API for filtering job runs and returning execution statistics. |
| [Job Registry with PostgreSQL](job-registry-postgresql/) | PostgreSQL schema and Python job manager for job states and execution metadata. |
| [CLI and API Integration](cli-api-integration/) | Authenticated REST requests through a Python command-line interface. |
| [Secure Webhook Receiver](secure-webhook-receiver/) | Flask endpoint with HMAC signature verification, JSON schema validation, and filtered event logging. |
| [Containerized Microservices](containerize-microservices/) | Docker Compose Flask API and worker services using Redis for task and result storage. |

### Configuration, Security, and Governance

| Project | Description |
|---|---|
| [Configuration Generator](config-generator/) | Generates environment-specific configuration from Jinja2 templates and YAML inputs, with schema checks. |
| [Typed Configuration Loader](typed-config-loader/) | Loads JSON and YAML configuration with Pydantic validation. |
| [Configuration Drift Scanner](config-drift-scanner/) | Compares system and application configuration with baselines and generates reports. |
| [Golden Configuration Enforcement](golden-config-enforcement/) | Compares current configuration with reference files and applies security policy checks. |
| [Dependency Policy and Safe Upgrades](dependency-policy-upgrades/) | Dependency policies, vulnerability scanning, validation tests, and upgrade recovery scripts. |
| [Compliance Evidence Generator](compliance-lab/) | Collects system evidence and produces structured JSON, HTML, and CSV reports. |
| [Multi-Profile Policy Gate](policy-gate-lab/) | Applies YAML-defined policy profiles through a lightweight HTTP service. |
| [Finance Approval Workflow](finance-approval-lab/approval-system/) | Threshold-based approval routing, multiple approvers, persisted request status, and audit events. |
| [Exploit Remediation and Regression Tests](exploit-fix-test/) | Demonstrates SQL injection remediation with parameterized queries and regression tests. |
| [Healthcare Log Sanitization](healthcare-logging-lab/) | Uses synthetic telemetry and masking checks to demonstrate handling of sensitive log fields. |

### Observability and Incident Response

| Project | Description |
|---|---|
| [Prometheus Metrics Instrumentation](prometheus-metrics-instrumentation/) | Flask application with request counters, latency histograms, gauges, health endpoint, and `/metrics`. |
| [Grafana Dashboard Evidence](grafana-dashboard-evidence/) | Prometheus and Node Exporter configuration with operational monitoring evidence files. |
| [Structured Logging and Correlation](structured-logging-correlation/) | JSON logging and correlation ID propagation across Flask services, with a log analysis utility. |
| [Simulated Incident Response](simulated-incident-drill/) | Bash and Python exercises for disk, service, and CPU incidents with action logs. |
| [Energy Telemetry and Threshold Detection](energy-pack-lab/energy-pack-lab/) | InfluxDB, Telegraf, and Kapacitor configuration for simulated energy metrics and threshold alerts. |
| [Manufacturing Telemetry and Downtime Alerts](manufacturing-monitor/) | InfluxDB telemetry collection, heartbeat-based downtime checks, and alert cooldown handling. |

### Reliability, Delivery, and Engineering Practices

| Project | Description |
|---|---|
| [Resilient HTTP Client](resilient-http-client/) | Requests-based client with timeouts, retry backoff, and optional circuit-breaker integration. |
| [Build and Version Artifacts](build-version-artifacts/) | Bash release scripts for semantic versions, tarball builds, SHA-256 metadata, and Git tags. |
| [Migration and Rollback Runbook](migration-rollback-runbook/) | PostgreSQL migration, pre-check, backup, restore, and validation scripts. |
| [Pre-commit Quality Gates](pre-commit-quality-gate/) | Local formatting, linting, security scanning, and file quality checks. |
| [Test Strategy](test-strategy-upgrade/) | Python unit and integration test structure using pytest and coverage reporting. |
| [AI-Driven Refactoring and Quality Metrics](ai-refactor-lab/) | Uses static analysis and tests to assess refactoring changes and code quality metrics. |
| [Retail Deployment Gate and Rollback](retail-deployment-lab/) | Deployment health checks and rollback-oriented scripts for a containerized service workflow. |

## Technology Overview

- **Languages:** Python, Bash, JavaScript
- **Web and API frameworks:** Flask, FastAPI
- **Task processing and data:** Celery, Redis, PostgreSQL, SQLite, InfluxDB
- **Containers and monitoring:** Docker, Prometheus, Node Exporter, Grafana, Telegraf, Kapacitor
- **AI-assisted workflows:** Ollama and local language models
- **Configuration and validation:** YAML, JSON Schema, Pydantic, Jinja2
- **Testing and security tooling:** pytest, pre-commit, Bandit, Safety, pip-audit

Technology choices and prerequisites vary by project; the list above describes tools used across the repository and does not imply a shared runtime.

## Getting Started

Clone the repository and open the project you want to explore:

```bash
git clone https://github.com/maazsheikh039/aiops-cloud-automation-suite.git
cd aiops-cloud-automation-suite
```

Each project directory contains its own README with setup requirements and operating instructions. Review those instructions before installing dependencies or running scripts. Several projects require external services or system utilities, such as Redis, PostgreSQL, Docker, Prometheus, Grafana, or InfluxDB.

## Repository Scope

This repository is a collection of independent projects and technical demonstrations. It does not provide a suite-wide installer or a single command to run every project. No repository-wide license file was present during this review.
