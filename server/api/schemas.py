from datetime import datetime

from database.datatypes import SensorType
from database.datatypes import VehicleStatus
from pydantic import BaseModel


class SensorData(BaseModel):
    sensor_type: SensorType
    timestamp: datetime
    sensor_data: float
    vehicle_serial: str


class VehicleStatusData(BaseModel):
    vehicle_serial: str
    vehicle_status: VehicleStatus
