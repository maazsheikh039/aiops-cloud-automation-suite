# Healthcare Secure Logging and PII Sanitization

## Objectives
- Automatically generate synthetic healthcare telemetry containing sensitive Patient Identifiable Information (PII).
- Implement robust masking routines for Social Security Numbers, emails, phone numbers, and names in accordance with HIPAA standards.
- Build automated regex validation suites to flag privacy violations and compliance failures in log files.
- Develop a production-ready JSON logger with real-time sanitization interceptors.

## Tools Used
- Python 3, Faker
- Python JSON Logger
- Regex Pattern Matchers & Hash Libraries
- Bash & Git

## Key Skills Demonstrated
- **Regulatory Compliance:** Engineering HIPAA-compliant logging pipelines to prevent sensitive data leaks.
- **Defensive Data Handling:** Sanitizing incoming JSON payloads and stripping unnecessary metadata (e.g., IP addresses).
- **Automated Validation Gates:** Running compliance checks as part of verification workflows.

## Troubleshooting Log
- **Regex Edge Cases:** Fine-tuned SSN and phone matching patterns to distinguish raw unmasked numbers from pre-masked indicators (`XXX-XX-`) during validation scans.
