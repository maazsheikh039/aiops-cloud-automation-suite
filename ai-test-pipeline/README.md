# AI Test Suggestion Pipeline

## Objectives
- Automatically analyze code modifications using Git diffs and Python Abstract Syntax Trees (AST).
- Calculate function complexity metrics (branches, loops, and cyclomatic complexity).
- Integrate local AI models (Ollama CodeLlama) to intelligently generate comprehensive unit test recommendations.
- Produce structured JSON artifacts and prioritized Markdown reports for CI/CD pipeline integration.

## Tools Used
- Python 3, GitPython
- Ollama (CodeLlama:7b Local LLM)
- Pytest / AST Parsing Module
- Bash & Git

## Key Skills Demonstrated
- **Automated QA Engineering:** Bridging static code analysis with generative AI for test gap detection.
- **AST-Driven Metadata Extraction:** Programmatically parsing code signatures, parameters, and complexity metrics.
- **CI/CD Quality Gates:** Automating test coverage recommendations per pull request without external API dependencies.

## Troubleshooting Log
- **Git Repository State:** Ensured graceful fallback logic in `CodeAnalyzer` to handle both bare git diff ranges and full directory file scans when evaluating local sample projects.
