# Templated Configuration Generator & Schema Validator

## Objectives
- Build a Python-based configuration generation pipeline utilizing Jinja2 templating and YAML data inputs.
- Implement multi-environment support (development vs. production) sharing reusable configuration templates.
- Enforce strict configuration standards using JSON Schema runtime validation.
- Provide syntax checks for generated infrastructure files like Nginx server blocks.

## Tools Used
- **Python 3**: Core generator and validator class architecture.
- **Jinja2**: Advanced templating engine supporting conditional blocks, loops, and default filters.
- **PyYAML & JSONSchema**: Parsing environment data and validating configuration instances.

## Key Skills Demonstrated
- **Infrastructure as Code (IaC)**: Decoupling configuration logic from environment-specific variables.
- **Data Governance**: Enforcing type safety and required parameters prior to deployment.
- **Templating Best Practices**: Utilizing block trimming and clean indentation management.
- **Automated Verification**: Building pre-flight syntax and schema validation gates.

## Troubleshooting Log
- **Issue**: Jinja2 throwing `TemplateNotFound` errors when locating template files.
  - **Resolution**: Configured `FileSystemLoader` with the absolute path relative to the `templates/` directory and ensured `.j2` file extensions.
- **Issue**: Strict schema validation failures due to missing optional attributes.
  - **Resolution**: Properly marked required properties in the JSON schema while utilizing Jinja2 `default()` filters for fallback values.
