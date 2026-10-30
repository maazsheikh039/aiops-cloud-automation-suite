# Energy Pack Ingestion and Threshold Detection

## Objectives
- Deploy and configure an enterprise observability stack comprising InfluxDB v2, Telegraf, and Kapacitor.
- Ingest real-time system metrics alongside custom simulated energy telemetry (wattage, voltage, current).
- Implement stream processing rules and threshold alerting via TICKscripts.
- Automate warning and critical incident logging for anomalous resource consumption.

## Tools Used
- InfluxDB v2 (Time-Series Database)
- Telegraf (Metrics Agent)
- Kapacitor (Stream Processing & Alerting Engine)
- Bash & Python

## Key Skills Demonstrated
- **Observability Pipeline Design:** Constructing end-to-end ingestion and alerting architectures for infrastructure metrics.
- **Stream Analytics:** Writing TICKscripts with sliding time windows to detect sustained metric threshold breaches.
- **Automated Incident Notification:** Routing warning and critical alerts to persistent audit logs.

## Troubleshooting Log
- **InfluxDB v2 Token Auth:** Ensured that Bearer/V2 API tokens generated during initial setup (`influx setup`) were properly mapped across Telegraf and Kapacitor configuration files to prevent unauthorized ingestion errors.
