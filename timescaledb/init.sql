CREATE TABLE IF NOT EXISTS resources (
    resource_id TEXT NOT NULL,
    resource_type_id TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    description TEXT NOT NULL,
    data_source_type TEXT NOT NULL,
    base_unit TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (resource_id)
);

CREATE TABLE IF NOT EXISTS readings (
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resource_id TEXT NOT NULL,
    reading_value TEXT NOT NULL,
    FOREIGN KEY (resource_id) REFERENCES resources (resource_id)
);

SELECT create_hypertable('readings', by_range('recorded_at'));