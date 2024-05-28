from dataclasses import dataclass


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
