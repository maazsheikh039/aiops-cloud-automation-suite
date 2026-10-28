# Multi-Layered Test Strategy Framework

A comprehensive testing architecture for Python applications utilizing `pytest`, strict decimal arithmetic, unit/integration separation, and automated code coverage reporting.

## Objectives
- Implement a multi-layered testing strategy (unit tests vs. integration workflows).
- Enforce robust precision calculations using Python's `Decimal` module for financial models.
- Validate component interactions and state consistency across inventory and order processing modules.
- Generate detailed code coverage metrics and HTML reports using `pytest-cov`.

## Tools Used
- **Pytest** for test execution, fixtures, and marker configuration
- **Pytest-Cov** for code coverage measurement
- **Python 3** (`dataclasses`, `decimal`, `typing`)
- **Linux Terminal** & Shell scripting

## Key Skills Demonstrated
- **Software Testing Quality:** Structuring isolated unit test suites alongside end-to-end integration tests.
- **Defensive Assertions:** Writing clear, descriptive assertions that pinpoint component failure states instantly.
- **Coverage Driven Development:** Tracking test metrics to ensure high test coverage (>80%) across production logic.

## Troubleshooting Log
- **Decimal Precision:** Ensured monetary subtotals and discounts use Python `Decimal` objects rather than floating-point numbers to prevent rounding errors.
- **Fixture Scoping:** Leveraged pytest fixtures for clean setup of inventory managers and sample products across test classes.
