# Golden Configuration Enforcement & Security Compliance Engine

## Objectives
- Establish immutable golden configuration templates for infrastructure services (Nginx, SSH).
- Implement automated compliance checking scripts using Python and `DeepDiff`.
- Detect drift, unapproved changes, and critical security policy violations (e.g., root login enabled).
- Provide pre-deployment blocking hooks and JSON-based audit trail reporting.

## Tools Used
- **Python 3**: Core comparison engine, security validation rules, and violation logging.
- **DeepDiff**: Precise recursive difference extraction between golden baselines and current configs.
- **PyYAML**: Parsing configuration datasets.
- **Shell Hooks**: Automated pre-deployment quality gates that block non-compliant execution.

## Key Skills Demonstrated
- **DevSecOps Policy Enforcement**: Integrating security governance directly into deployment workflows.
- **Configuration Drift Management**: Catching unauthorized state mutations against known-good baselines.
- **Audit & Compliance Reporting**: Maintaining timestamped JSON violation ledgers for auditing.
- **Quality Gate Automation**: Halting CI/CD pipelines when configuration standards are breached.

## Troubleshooting Log
- **Issue**: Mismatched filenames causing validation skips during automated batch checks.
  - **Resolution**: Created explicit dictionary mappings linking current files to their respective golden baseline templates.
- **Issue**: Security checks missing nested dictionary keys.
  - **Resolution**: Implemented safe dictionary `.get()` lookups with default fallbacks to prevent `KeyError` crashes on incomplete configurations.
