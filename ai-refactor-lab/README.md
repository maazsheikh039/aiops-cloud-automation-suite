# AI-Driven Refactoring with Code Quality Metrics

## Objectives
- Measure legacy code complexity and maintainability using static analysis (`Radon`).
- Apply structural refactoring patterns (Strategy Pattern, early returns) to reduce cyclomatic complexity.
- Validate functional equivalence through comprehensive parameterized correctness testing (`pytest`).
- Monitor execution performance before and after refactoring (`pytest-benchmark`).

## Tools Used
- Python 3, Radon, Pylint
- Pytest & Pytest-Benchmark
- Git & Bash

## Key Skills Demonstrated
- **Code Quality Engineering:** Quantifying technical debt and reducing cyclomatic complexity by >50%.
- **Design Pattern Application:** Replacing complex nested conditional logic with extensible object-oriented strategy classes.
- **Automated Verification:** Ensuring zero regression during refactoring via rigorous test assertions.

## Troubleshooting Log
- **Threshold Tuning:** Calibrated parameterized test cases to handle floating-point rounding precision differences when comparing legacy flat functions against modular strategy calculations.
