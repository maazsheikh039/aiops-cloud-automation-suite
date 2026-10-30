# CI Failure Triage Assistant

## Objectives
- Automatically parse and analyze CI/CD build logs for common failure signatures.
- Implement extensible pattern matching driven by external YAML configurations.
- Extract error lines with surrounding context for rapid developer diagnosis.
- Process multiple log files concurrently in batch mode for pipeline reporting.

## Tools Used
- Python 3, PyYAML, Colorama
- Bash & Git

## Key Skills Demonstrated
- **CI/CD Automation:** Reducing mean time to resolution (MTTR) for failed build pipelines.
- **Log Parsing & Pattern Matching:** Building robust text inspection engines with confidence scoring.
- **Configuration-Driven Design:** Decoupling detection patterns from core inspection logic via YAML.

## Troubleshooting Log
- **Encoding & ANSI Colors:** Initialized `colorama.init(autoreset=True)` to ensure cross-platform colored output rendering in terminal and CI environments.
