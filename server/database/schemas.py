from enum import Enum


class SensorType(Enum):
    """Enum for different types of sensors used in vehicles.

    Attributes:
        TEMPERATURE (str): Represents a temperature sensor.
        WEIGHT (str): Represents a weight sensor.
        FUEL (str): Represents a fuel level sensor.
    """

    TEMPERATURE = "temperature"
    WEIGHT = "weight"
    FUEL = "fuel"


class VehicleStatus(Enum):
    """Enum for different status states of a vehicle.

    Attributes:
        ACTIVE (str): Indicates the vehicle is active.
        INACTIVE (str): Indicates the vehicle is inactive.
        MAINTENANCE (str): Indicates the vehicle is under maintenance.
        ERROR (str): Indicates the vehicle has an error.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ERROR = "error"
