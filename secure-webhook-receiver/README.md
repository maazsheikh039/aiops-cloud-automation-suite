# Secure Webhook Receiver with HMAC Verification & Schema Validation

## Objectives
- Implement secure cryptographic webhook signature verification using HMAC-SHA256 and constant-time comparisons (`hmac.compare_digest`).
- Enforce strict JSON schema validation (`jsonschema`) to reject malformed payloads before processing.
- Build secure, structured audit logging that sanitizes sensitive secrets (passwords, API tokens) from log streams.
- Expose health-check and protected webhook endpoints using Flask.

## Tools Used
- **Python & Flask**: Lightweight application framework and request routing.
- **HMAC / Hashlib**: Cryptographic message authentication and signature hashing.
- **JsonSchema**: Declarative structure validation for incoming API requests.

## Key Skills Demonstrated
- **API Security**: Defending webhook endpoints against replay, spoofing, and timing attacks.
- **Input Validation**: Ensuring untrusted external payloads comply with rigorous schema rules.
- **Audit Compliance**: Maintaining structured logs while protecting user privacy and credential safety.
