# Typed Configuration Loader

A production-grade, schema-validated configuration management library built with Pydantic for Python applications and cloud automation pipelines.

## Objectives
- Implement type-safe configuration loading supporting both JSON and YAML formats.
- Enforce strict validation schemas, data type constraints, and custom field validators.
- Apply sensible defaults for missing optional parameters to reduce configuration overhead.
- Support live configuration reloading and graceful error handling.

## Tools Used
- **Python 3** (`pydantic`, `yaml`, `json`, `os`)
- **Pytest / Custom Test Runner** for schema validation testing
- **Linux Terminal** & Shell environment

## Key Skills Demonstrated
- **Schema Validation:** Defining robust configuration contracts using Pydantic models and field constraints (`ge`, `le`, custom validators).
- **Defensive Engineering:** Catching type mismatches, missing required attributes, and invalid environment parameters before runtime.
- **Multi-Format Parsing:** Handling structured text configs seamlessly across JSON and YAML parsers.

## Troubleshooting Log
- **Pydantic Version Compatibility:** Utilized standard `@validator` decorators for clean data coercion and error reporting.
- **File Extension Routing:** Implemented dynamic parsing branch selection based on file extensions (`.json`, `.yaml`, `.yml`).
