# Prometheus Metrics Instrumentation & Observability Platform

## Objectives
- Deploy and configure Prometheus time-series database and scrape targets.
- Instrument a Python Flask application with key SRE metric types: **Counters** (cumulative request counts), **Gauges** (active connections & health scores), and **Histograms** (latency distribution buckets).
- Expose standardized Prometheus metrics via an HTTP `/metrics` endpoint.
- Simulate application traffic and validate scrape targets via Prometheus APIs.

## Tools Used
- **Prometheus & Promtool**: Time-series scraping, monitoring engine, and configuration syntax validation.
- **Python Flask & `prometheus-client`**: Application framework and native metric instrumentation decorators.
- **Systemd**: Managing persistent background system services.

## Key Skills Demonstrated
- **Application Observability**: Instrumenting microservices with production-grade telemetry.
- **Metric Type Selection**: Correctly applying Counters vs. Gauges vs. Histograms for system monitoring.
- **Scrape Target Configuration**: Setting up interval-based polling and health checking targets in Prometheus.
