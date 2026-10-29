# Structured Logging & Distributed Correlation ID Propagation

## Objectives
- Implement structured JSON logging (`python-json-logger`) ensuring uniform log parsing fields (`asctime`, `levelname`, `correlation_id`, `message`).
- Establish a request middleware pattern in Flask (`@app.before_request`) to extract incoming `X-Correlation-ID` headers or generate unique UUIDs.
- Propagate correlation IDs seamlessly across downstream microservice HTTP boundaries using request headers.
- Build automated log analysis utilities to group and trace request flows across multiple distributed services.

## Tools Used
- **Python / Flask**: Web application framework and request context middleware (`flask.g`).
- **Python JSON Logger**: Formatter for structured JSON log output.
- **Requests Library**: HTTP client used for downstream service communication and header forwarding.

## Key Skills Demonstrated
- **Distributed Observability**: Tracing end-to-end request lifecycles across decoupled microservices.
- **Contextual Logging**: Injecting request-scoped metadata into log streams without polluting business logic.
- **Centralized Log Analysis**: Parsing JSON event streams to reconstruct distributed execution traces.
