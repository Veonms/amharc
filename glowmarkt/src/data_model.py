from dataclasses import dataclass
from typing import Optional


@dataclass
class Credentials:
    bright_username: str
    bright_password: str
    bright_application_id: str
    valkey_host: str
    valkey_port: str


@dataclass
class CachedCredentials:
    bright_veid: Optional[str]
    bright_token: Optional[str]


@dataclass
class DateRange:
    start_date: str
    end_date: str


@dataclass
class Resource:
    resource_type_id: str
    name: str
    type: str
    description: str
    data_source_type: str
    base_unit: str
    resource_id: str
    created_at: str


@dataclass
class Reading:
    recorded_at: str
    resource_id: str
    reading_value: float
