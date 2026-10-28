# Job Registry with PostgreSQL

A production-grade Python and PostgreSQL job registry and state tracking engine designed for automated workflow orchestration and AIOps platforms.

## Objectives
- Design a relational PostgreSQL schema with optimized indexes for job persistence and timeline tracking.
- Implement explicit transaction management (`commit`, `rollback`) for state transitions (`pending` $\rightarrow$ `running` $\rightarrow$ `completed`/`failed`).
- Store unstructured execution metrics and summaries as structured JSONB data.
- Calculate job durations and query execution history by status.

## Tools Used
- **PostgreSQL** for relational metadata and JSONB storage
- **Psycopg2** for Python database connectivity and RealDictCursor parsing
- **Linux Terminal** & Shell environment

## Key Skills Demonstrated
- **Persistence Architecture:** Designing robust database schemas with indexing for time-series and state querying.
- **Transaction Safety:** Enforcing atomic updates and preventing partial database corruption on execution failures.
- **JSONB Querying:** Storing arbitrary execution metadata natively in PostgreSQL for audit reporting.
