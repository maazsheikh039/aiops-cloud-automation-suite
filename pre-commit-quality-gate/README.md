# Pre-commit Quality Gate Framework

A robust DevSecOps automation setup utilizing pre-commit hooks to enforce code formatting, linting, security vulnerability scanning, and file integrity standards prior to Git commits.

## Objectives
- Configure pre-commit hooks to automate code quality enforcement locally.
- Implement automated code formatting with Black and linting with Flake8.
- Integrate security vulnerability scanning using Bandit.
- Enforce file formatting and size standards for JSON and YAML configurations.

## Tools Used
- **Pre-commit Framework** for Git hook orchestration
- **Black** for opinionated Python code formatting
- **Flake8** for Python style guide and syntax linting
- **Bandit** for static security analysis of Python code
- **Linux Terminal** & Git

## Key Skills Demonstrated
- **DevSecOps Quality Gates:** Shifting security and quality checks left into the developer's local commit workflow.
- **Automated Remediation:** Utilizing hooks that auto-format code and catch errors before code review.
- **Custom Hook Engineering:** Writing custom local hooks to scan for unresolved TODO items and ensure repository cleanliness.

## Troubleshooting Log
- **Path Resolution:** Ensured pip binary paths are correctly exported in shell configurations if pre-commit commands are not found.
- **Formatter Conflicts:** Configured `.flake8` with `extend-ignore = E203, W503` to prevent rule conflicts with Black formatting.
