# Finance Pack Audit and Approval Gate

## Objectives
- Implement threshold-based approval gates for financial operations and infrastructure deployments.
- Enforce multi-approver sign-off policies (e.g., Finance Manager & Team Lead validation).
- Secure compliance tracking with append-only JSON audit logging.
- Provide CLI management tools for audit querying and request status verification.

## Tools Used
- Python 3, PyYAML
- JSON State & Audit Logging Stores
- Bash & Git

## Key Skills Demonstrated
- **FinOps & Governance:** Building programmatic compliance gates for budget-sensitive deployment pipelines.
- **Audit Logging Architecture:** Structuring immutable timestamped event logs for regulatory compliance.
- **Workflow State Management:** Tracking multi-party authorization progression across gate thresholds.

## Troubleshooting Log
- **State Persistence:** Implemented local JSON state serialization (`approval_state.json`) to persist multi-step approval increments between CLI invocations.
