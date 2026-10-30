# Manufacturing Telemetry Collector and Downtime Alerts

## Objectives
- Implement real-time industrial equipment telemetry generation and time-series ingestion using InfluxDB.
- Build continuous downtime detection watchers evaluating machine health status and heartbeat signals.
- Configure throttled alert mechanisms with cooldown periods to prevent alert fatigue.
- Provide HTTP webhook receivers for external incident notification integration.

## Tools Used
- Python 3, InfluxDB Client & Server
- Telegraf Telemetry Agent
- Bash & Git

## Key Skills Demonstrated
- **Industrial IoT (IIoT) Monitoring:** Capturing and storing high-frequency machine metrics in time-series databases.
- **Proactive Failure Detection:** Implementing threshold and heartbeat checks for automated incident response.
- **Alert Fatigue Mitigation:** Designing intelligent notification cooldown systems for production environments.

## Troubleshooting Log
- **InfluxDB Authentication & Buckets:** Configured legacy InfluxDB 1.x compatibility mappings (`manufacturing/autogen`) to seamlessly ingest Python client points into time-series tables.
