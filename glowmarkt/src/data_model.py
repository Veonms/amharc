from dataclasses import dataclass


@dataclass
class Credentials:
    bright_username: str
    bright_password: str
    bright_application_id: str
    valkey_host: str
    valkey_port: str


@dataclass
class Resource:
    resourceTypeId: str
    name: str
    type: str
    description: str
    dataSourceType: str
    baseUnit: str
    resourceId: str
    createdAt: str


@dataclass
class Reading:
    timestamp: str
    resourceId: str
    value: float
