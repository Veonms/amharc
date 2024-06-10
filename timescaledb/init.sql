CREATE TABLE IF NOT EXISTS resources (
    resourceId varchar(255) NOT NULL,
    resourceTypeId varchar(255) NOT NULL,
    name varchar(255) NOT NULL,
    type varchar(255) NOT NULL,
    description varchar(255) NOT NULL,
    dataSourceType varchar(255) NOT NULL,
    baseUnit varchar(255) NOT NULL,
    createdAt TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (resourceId)
);

CREATE TABLE IF NOT EXISTS readings (
    recordedAt TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resourceId varchar(255) NOT NULL,
    readingValue varchar(255) NOT NULL,
    FOREIGN KEY (resourceId) REFERENCES resources (resourceId)
);