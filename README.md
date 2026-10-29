# AIOps Cloud Automation Suite

### Cloud Operations · Automation · Platform Engineering

A portfolio of practical projects for building and operating dependable cloud and platform workflows. Explore automation services, configuration controls, job orchestration, reliability patterns, and delivery tooling—all organized as independent projects.

[![Python](https://img.shields.io/badge/Python-Projects-3776AB?logo=python&logoColor=white)](#project-directory)
[![Docker](https://img.shields.io/badge/Docker-Selected%20projects-2496ED?logo=docker&logoColor=white)](#project-directory)
[![Platform Engineering](https://img.shields.io/badge/Focus-Platform%20Engineering-7357D5)](#project-areas)

---

## At a Glance

| Projects | Focus areas | Languages and tools |
|:--:|:--:|:--|
| **18** | Automation, APIs, configuration, reliability, delivery | Python, Bash, Docker, PostgreSQL, SQLite, Redis |

## Project Areas

| Area | Includes |
|---|---|
| **APIs & Services** | Health and policy endpoints, job history APIs, CLI-to-API integration |
| **Automation & Orchestration** | Async execution, dependency-aware pipelines, background workers |
| **Configuration & Governance** | Typed configuration, template generation, drift detection, golden configuration checks |
| **Containers & Data** | Docker Compose microservices, PostgreSQL job registry, SQLite-backed queue |
| **Reliability & Delivery** | Resilient HTTP requests, artifact versioning, migration runbooks, pre-commit checks, testing strategy |

## Project Directory

### APIs & Services

| Project | Overview |
|---|---|
| [FastAPI Status and Policy Service](fastapi-status-policy-service/) | Health checks, system metrics, request validation, and policy enforcement. |
| [Job History API](job-history-api/) | Searchable execution history and job statistics through a Flask API. |
| [CLI and API Integration](cli-api-integration/) | Authenticated REST API access from a structured command-line interface. |

### Automation & Orchestration

| Project | Overview |
|---|---|
| [Async Execution Engine](async-execution-engine/) | Async task queues, worker pools, lifecycle states, and execution monitoring. |
| [Pipeline Runner](pipeline-runner/) | YAML-defined jobs with dependency ordering and failure propagation. |
| [Worker Service](worker-service/) | API-backed persistent queue for asynchronous operational jobs. |
| [Opsctl CLI](opsctl-core/) | Extensible command-line foundation for common operational tasks. |

### Configuration & Governance

| Project | Overview |
|---|---|
| [Configuration Generator](config-generator/) | Environment-aware configuration from reusable templates with schema validation. |
| [Typed Configuration Loader](typed-config-loader/) | JSON and YAML loading with typed validation and defaults. |
| [Configuration Drift Scanner](config-drift-scanner/) | Baseline comparison with structured compliance and drift reports. |
| [Golden Configuration Enforcement](golden-config-enforcement/) | Golden-state checks and security policy validation for configuration changes. |

### Containers, Data & Reliability

| Project | Overview |
|---|---|
| [Containerized Microservices](containerize-microservices/) | Docker Compose API and worker services connected through Redis. |
| [Job Registry with PostgreSQL](job-registry-postgresql/) | Persistent job states, transactional updates, and JSONB execution metadata. |
| [Resilient HTTP Client](resilient-http-client/) | Timeouts, retry backoff, and circuit-breaker behavior for HTTP requests. |

### Delivery & Engineering Practices

| Project | Overview |
|---|---|
| [Build and Version Artifacts](build-version-artifacts/) | Semantic versions, packaged artifacts, checksums, and build metadata. |
| [Migration and Rollback Runbook](migration-rollback-runbook/) | PostgreSQL migration tracking, pre-flight checks, backup, and recovery guidance. |
| [Pre-commit Quality Gates](pre-commit-quality-gate/) | Automated formatting, linting, security checks, and file standards. |
| [Test Strategy Upgrade](test-strategy-upgrade/) | Unit and integration testing structure with coverage reporting. |

## Technology Overview

**Languages:** Python, Bash  
**APIs and frameworks:** Flask, FastAPI, Click  
**Infrastructure and data:** Docker Compose, Redis, PostgreSQL, SQLite  
**Configuration and validation:** YAML, JSON Schema, Pydantic, Jinja2  
**Quality and reliability:** pytest, pre-commit, Bandit, retries, circuit breakers

## Getting Started

Clone the repository, then open the project you want to explore:

```bash
git clone https://github.com/maazsheikh039/aiops-cloud-automation-suite.git
cd aiops-cloud-automation-suite
```

Each project has its own README with its prerequisites and run instructions. Dependencies and services differ by project, so follow the documentation inside the selected directory.

## Repository Structure

The repository contains independent project directories. There is no suite-wide install command; start with the README inside the project you choose.

## License

A repository-wide license was not confirmed when this overview was prepared. Add the applicable license details here if you plan to publish reuse terms.
