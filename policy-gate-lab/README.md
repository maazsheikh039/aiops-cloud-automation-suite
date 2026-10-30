# Multi-Profile Policy Gate

## Objectives
- Implement a multi-profile policy enforcement engine capable of handling distinct regulatory frameworks (HIPAA, PCI-DSS, General Commerce).
- Provide dynamic profile switching via REST APIs without restarting services.
- Enforce strict rules (encryption, access logging, password complexity, rate limiting) based on active industry profiles.
- Maintain persistent active profile configurations.

## Tools Used
- Python 3, PyYAML, Requests
- Python Built-in HTTP Server (`http.server`)
- Bash & Git

## Key Skills Demonstrated
- **Policy as Code (PaC):** Abstracting compliance rules into declarative YAML profiles.
- **Dynamic Configuration Management:** Switching active security postures on-the-fly in multi-tenant environments.
- **RESTful Gate Architecture:** Building lightweight inspection proxies for inbound system requests.

## Troubleshooting Log
- **Background Server Management:** Managed background Python HTTP server lifecycle with clean background process termination during automated test runs.
