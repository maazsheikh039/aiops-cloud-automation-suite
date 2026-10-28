# Resilient HTTP Client Library

A robust, fault-tolerant Python HTTP client library featuring exponential backoff retries, strict timeout management, HTTP error classification, and Circuit Breaker pattern integration.

## Objectives
- Implement intelligent retry logic for transient network failures and rate limits (HTTP 429).
- Configure exponential backoff strategies to prevent overwhelming upstream services.
- Enforce strict request timeouts to prevent indefinite hanging in automation pipelines.
- Integrate the Circuit Breaker pattern to isolate faults and prevent cascading microservice failures.

## Tools Used
- **Requests Library** for HTTP operations
- **Python 3** (`time`, `logging`, `enum`, `typing`)
- **Linux Terminal** & Shell environment

## Key Skills Demonstrated
- **Fault Tolerance Engineering:** Designing resilient network wrappers that handle intermittent connectivity issues gracefully.
- **Backoff & Jitter Optimization:** Utilizing exponential math to stagger retry attempts efficiently.
- **Circuit Breaker State Management:** Managing CLOSED, OPEN, and HALF_OPEN states to safeguard distributed systems.

## Troubleshooting Log
- **DNS Resolution:** Verified local DNS resolution for testing endpoints (`httpbin.org`).
- **Threshold Tuning:** Adjusted failure thresholds in the circuit breaker test to ensure rapid state transitions during test runs.
