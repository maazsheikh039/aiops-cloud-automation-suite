# AIOps Cloud Automation Suite

### Cloud Operations · Automation · Platform Engineering

A collection of focused projects for automating and operating cloud and platform workflows. The repository brings together job orchestration, service APIs, configuration governance, observability, security controls, and delivery practices.

[![Python](https://img.shields.io/badge/Python-Projects-3776AB?logo=python&logoColor=white)](#technology-overview)
[![Automation](https://img.shields.io/badge/Focus-Automation-7357D5)](#project-areas)
[![Observability](https://img.shields.io/badge/Focus-Observability-EE7623)](#project-areas)

---

## At a Glance

| Projects | Project areas | Technologies |
|:--:|:--|:--|
| **25** | APIs, automation, configuration, security, observability, reliability, delivery | Python, Bash, Node.js, Docker, PostgreSQL, SQLite, Redis, Prometheus, Grafana |

## Project Areas

| Area | What you will find |
|---|---|
| **APIs & Services** | Health and policy endpoints, job history, command-line API access, and webhook handling |
| **Automation & Orchestration** | Async task execution, dependency-aware pipelines, background workers, and deployment smoke checks |
| **Configuration & Governance** | Typed configuration, template generation, drift detection, and golden configuration checks |
| **Observability & Incident Response** | Prometheus metrics, Grafana monitoring setup, structured correlation logs, and incident drills |
| **Reliability & Delivery** | Resilient HTTP requests, dependency checks, artifact metadata, database migration procedures, quality gates, and test strategy |
| **Containers & Data** | Docker Compose services, PostgreSQL job tracking, Redis queues, and SQLite-backed job history |

## Project Directory

### APIs & Services

| Project | Overview |
|---|---|
| [FastAPI Status and Policy Service](fastapi-status-policy-service/) | Health and system metrics endpoints with request validation, policy checks, and request logging. |
| [Job History API](job-history-api/) | Flask and SQLAlchemy API for filtering job runs and returning execution statistics. |
| [CLI and API Integration](cli-api-integration/) | Authenticated REST requests through a Python command-line interface. |
| [Secure Webhook Receiver](secure-webhook-receiver/) | Flask webhook endpoint with HMAC-SHA256 signature checks, JSON schema validation, and sanitized event logging. |

### Automation & Orchestration

| Project | Overview |
|---|---|
| [Async Execution Engine](async-execution-engine/) | Python asyncio worker pool with queued tasks, lifecycle states, and execution statistics. |
| [Pipeline Runner](pipeline-runner/) | YAML-configured jobs with dependency ordering, cycle checks, and downstream failure handling. |
| [Worker Service](worker-service/) | Flask API and SQLite-backed queue for asynchronous operational jobs. |
| [Opsctl CLI](opsctl-core/) | Modular Python CLI for status, deployment, and local configuration commands. |
| [Smoke Test Pipeline](smoke-test-pipeline/) | Shell-driven deployment flow that checks a Node.js service's health and API endpoints. |

### Configuration & Governance

| Project | Overview |
|---|---|
| [Configuration Generator](config-generator/) | Jinja2 templates and YAML inputs for generating environment-specific configuration, with schema checks. |
| [Typed Configuration Loader](typed-config-loader/) | JSON/YAML configuration parsing with Pydantic validation. |
| [Configuration Drift Scanner](config-drift-scanner/) | Baseline comparisons for system and application configuration with JSON/text reports. |
| [Golden Configuration Enforcement](golden-config-enforcement/) | Configuration comparison and security policy checks against known-good files. |

### Observability & Incident Response

| Project | Overview |
|---|---|
| [Prometheus Metrics Instrumentation](prometheus-metrics-instrumentation/) | Flask service exposing request counters, latency histograms, gauges, health, and a `/metrics` endpoint. |
| [Grafana Dashboard Evidence](grafana-dashboard-evidence/) | Prometheus and Node Exporter configuration with operational monitoring evidence files. |
| [Structured Logging & Correlation](structured-logging-correlation/) | JSON logs and correlation ID propagation across two Flask services, with a log analysis utility. |
| [Simulated Incident Drill](simulated-incident-drill/) | Bash/Python exercises for disk, service, and CPU incident response with action logs. |

### Reliability, Data & Delivery

| Project | Overview |
|---|---|
| [Containerized Microservices](containerize-microservices/) | Docker Compose Flask API and worker services using Redis as a task queue and result store. |
| [Job Registry with PostgreSQL](job-registry-postgresql/) | PostgreSQL schema and Python job manager for job state transitions and execution metadata. |
| [Resilient HTTP Client](resilient-http-client/) | Requests-based client with timeouts, retry backoff, and optional circuit-breaker integration. |
| [Dependency Policy & Safe Upgrades](dependency-policy-upgrades/) | Dependency policy configuration, vulnerability scanning commands, tests, and upgrade/rollback scripts. |
| [Build and Version Artifacts](build-version-artifacts/) | Bash scripts for semantic versions, tarball builds, SHA-256 metadata, and Git tags. |
| [Migration and Rollback Runbook](migration-rollback-runbook/) | PostgreSQL migration, pre-check, backup, restore, and validation scripts. |
| [Pre-commit Quality Gates](pre-commit-quality-gate/) | Configuration and sample app for local formatting, linting, security, and file checks. |
| [Test Strategy Upgrade](test-strategy-upgrade/) | Python unit/integration test structure using pytest and coverage reporting. |

## Technology Overview

**Languages:** Python, Bash, JavaScript  
**Web and API frameworks:** Flask, FastAPI  
**Containers and data:** Docker Compose, Redis, PostgreSQL, SQLite  
**Observability:** Prometheus, Node Exporter, Grafana, JSON logging  
**Configuration and validation:** YAML, JSON Schema, Pydantic, Jinja2  
**Quality and security tooling:** pytest, pre-commit, Bandit, Safety, pip-audit

## Getting Started

Clone the repository and choose a project directory:

```bash
git clone https://github.com/maazsheikh039/aiops-cloud-automation-suite.git
cd aiops-cloud-automation-suite
```

Each project is maintained in its own folder and has its own README. Review that project's prerequisites and instructions before installing dependencies or running scripts. Some examples require services such as Docker, Redis, PostgreSQL, Prometheus, or Grafana.

## Repository Structure

```text
aiops-cloud-automation-suite/
├── async-execution-engine/
├── build-version-artifacts/
├── cli-api-integration/
├── config-drift-scanner/
├── config-generator/
├── containerize-microservices/
├── dependency-policy-upgrades/
├── fastapi-status-policy-service/
├── golden-config-enforcement/
├── grafana-dashboard-evidence/
├── job-history-api/
├── job-registry-postgresql/
├── migration-rollback-runbook/
├── opsctl-core/
├── pipeline-runner/
├── pre-commit-quality-gate/
├── prometheus-metrics-instrumentation/
├── resilient-http-client/
├── secure-webhook-receiver/
├── simulated-incident-drill/
├── smoke-test-pipeline/
├── structured-logging-correlation/
├── test-strategy-upgrade/
├── typed-config-loader/
└── worker-service/
```

## Scope & License

These are independent projects and examples; they do not share a suite-wide installer or runtime. Check each project README for its local setup and constraints. No repository-wide license file was present during this review.
