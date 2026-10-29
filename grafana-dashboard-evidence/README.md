# Grafana Operational Dashboards & Prometheus Monitoring Stack

## Objectives
- Deploy and configure an end-to-end production monitoring stack (Prometheus, Node Exporter, Grafana OSS).
- Set up Prometheus as a robust time-series data source inside Grafana.
- Design operational dashboards tracking critical system vitals: CPU idle rates, memory usage, disk footprints, and network throughput.
- Automate evidence packaging, metrics auditing, and configuration backups for compliance reviews.

## Tools Used
- **Prometheus**: Time-series database and metrics collection scraper (`prometheus-config.yml`).
- **Node Exporter**: Bare-metal hardware and OS metrics telemetry agent (`node_exporter.service`).
- **Grafana OSS**: Visualization platform and dashboard authoring UI.

## Evidence Package Contents
- `README.md`: Lab documentation and architecture overview.
- `metrics-summary.txt`: Live snapshot of system performance metrics and service states.
- `prometheus-config.yml`: Scrape target configurations for Prometheus.
- `node_exporter.service`: Systemd configuration for hardware metric collection.
