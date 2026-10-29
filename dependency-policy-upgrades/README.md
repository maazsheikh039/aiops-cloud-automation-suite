# Dependency Policy & Safe Upgrade Automation Pipeline

## Objectives
- Define strict dependency upgrade policies, schedules, and version constraints (`dependency-policy.yaml`).
- Implement automated vulnerability scanning using `safety` and `pip-audit` for CVE detection.
- Build comprehensive pytest test suites to validate application behavior post-upgrade.
- Create automated fail-safe upgrade scripts with built-in environment backup and rollback capabilities.

## Tools Used
- **Python & Pytest**: Application logic and automated unit test execution.
- **Safety & Pip-Audit**: Software Bill of Materials (SBOM) and vulnerability scanners.
- **Bash Scripting**: Backup routines, upgrade validation workflows, and automated rollbacks.

## Key Skills Demonstrated
- **Supply Chain Security**: Proactively detecting and mitigating open-source vulnerabilities.
- **Risk Mitigation**: Enforcing strict testing and rollback protocols before production deployment.
- **Policy Automation**: Codifying organizational dependency rules into maintainable configuration files.
