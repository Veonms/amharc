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
    recordedAt: str
    resourceId: str
    readingValue: float
