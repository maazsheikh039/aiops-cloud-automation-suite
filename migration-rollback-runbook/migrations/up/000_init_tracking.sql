CREATE TABLE IF NOT EXISTS migration_history (
    id SERIAL PRIMARY KEY,
    migration_name VARCHAR(255) NOT NULL,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    executed_by VARCHAR(100),
    rollback_at TIMESTAMP,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_migration_name ON migration_history(migration_name);
CREATE INDEX IF NOT EXISTS idx_executed_at ON migration_history(executed_at);
