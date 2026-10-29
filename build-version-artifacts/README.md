# Semantic Versioning, Artifact Build, and Provenance Pipeline

## Objectives
- Implement automated semantic versioning (`MAJOR.MINOR.PATCH`) with bash-driven release managers.
- Package application source files into immutable tarball artifacts.
- Generate structured build metadata including SHA-256 checksums, timestamps, and builder fingerprints.
- Associate builds with immutable, annotated Git release tags for end-to-end traceability.

## Tools Used
- **Bash Scripting**: Automated version bumping, tarball creation, and release workflows.
- **Git Tags**: Release point annotation and commit tracing.
- **`jq`**: Structured JSON metadata manipulation and querying.
- **SHA-256**: Cryptographic checksum generation and verification.

## Key Skills Demonstrated
- **Release Engineering**: Standardizing software release lifecycles and semantic versioning rules.
- **Artifact Traceability**: Tying built deliverables directly to source control commits and build environments.
- **Integrity Verification**: Automated checksum validation preventing tampering or corruption during transit.
