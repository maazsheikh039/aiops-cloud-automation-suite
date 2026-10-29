# Configuration Drift Scanner & Compliance Auditor

## Objectives
- Implement an automated system and application configuration drift detection engine.
- Capture immutable system baselines (hosts, packages, services, network interfaces).
- Perform deep semantic comparison on YAML configurations using `DeepDiff` and SHA256 cryptographic hashing.
- Generate structured JSON and human-readable audit reports for CI/CD compliance gates.

## Tools Used
- **Python 3**: Core drift detection class architecture, file hashing, and reporting.
- **DeepDiff**: Advanced recursive dictionary and list comparison for structured YAML configurations.
- **PyYAML**: Parsing and serializing configuration state structures.
- **Shell Scripting**: Automating baseline snapshots and current state capture pipelines.

## Key Skills Demonstrated
- **Compliance & Governance**: Ensuring production infrastructure aligns strictly with declared specifications.
- **State Auditing**: Detecting unauthorized or undocumented configuration mutations across servers.
- **CI/CD Quality Gates**: Integrating automated scanning scripts that block deployments when drift is identified.
- **Error Handling & Hashing**: Utilizing SHA256 integrity checks and robust exception handling.

## Troubleshooting Log
- **Issue**: Missing Python dependencies when executing the scanner in clean virtual environments.
  - **Resolution**: Pinned exact package versions for `pyyaml` and `deepdiff` in requirements setup to ensure consistent environment execution.
- **Issue**: YAML key ordering causing false positives in comparison checks.
  - **Resolution**: Enabled `ignore_order=True` inside `DeepDiff` parameters to evaluate structural content equality regardless of key arrangement.
