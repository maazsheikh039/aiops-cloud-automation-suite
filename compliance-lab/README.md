# Government Enterprise Pack Compliance Evidence Generator

## Objectives
- Automate the collection of compliance artifacts (system logs, user access records, and configuration snapshots).
- Produce multi-format compliance reports (JSON, HTML, and CSV) structured for frameworks like NIST 800-53.
- Maintain immutable, structured audit trails (`audit.log` and `audit.json`) for verification.
- Provide a robust orchestration workflow coordinating evidence harvesting, reporting, and logging.

## Tools Used
- Python 3, PyYAML, Jinja2, Python-Dateutil
- System Utilities (`journalctl`, `systemctl`, `last`, `ip`)
- Bash & Git

## Key Skills Demonstrated
- **Automated Governance & Auditing:** Programmatically gathering compliance evidence without manual intervention.
- **Multi-Format Report Generation:** Rendering structured telemetry into developer-friendly and stakeholder-ready reports.
- **Compliance Pipeline Orchestration:** Ensuring complete auditability and error-resilient execution in regulated environments.

## Troubleshooting Log
- **Subprocess Execution Limits:** Configured timeouts and fallback exception handlers when querying system logs in restricted bare-metal environments.
