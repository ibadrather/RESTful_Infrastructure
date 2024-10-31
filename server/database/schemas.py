from enum import Enum


class SensorType(Enum):
    TEMPERATURE = "temperature"
    WEIGHT = "weight"
    FUEL = "fuel"


class VehicleStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ERROR = "error"
