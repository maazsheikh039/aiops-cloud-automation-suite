# AI-Assisted Automated Runbook Generator

## Objectives
- Automatically collect live Linux system telemetry (OS, kernel, CPU, disk, services, and ports).
- Integrate local AI language models (Ollama with Llama 3.2) for secure, offline incident remediation generation.
- Programmatically construct standardized operational procedures in Markdown and YAML formats using Jinja2 templates.
- Streamline DevOps incident response workflows with automated documentation.

## Tools Used
- Python 3, Requests, PyYAML, Jinja2
- Ollama (Local LLM Engine)
- Linux System Utilities (`sysstat`, `procps`, `iproute2`)
- Git & Bash

## Key Skills Demonstrated
- **AIOps Automation:** Bridging live system diagnostics with generative AI for rapid incident response.
- **Context-Aware Prompt Engineering:** Structuring system context payloads for precise LLM troubleshooting output.
- **Template-Driven Documentation:** Rendering structured JSON telemetry into clean, professional Markdown and YAML artifacts.

## Troubleshooting Log
- **Ollama Service Management:** Handled background service initialization using `ollama serve &` with sleep intervals to guarantee REST API readiness before Python requests.
