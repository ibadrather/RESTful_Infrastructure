from typing import List
from typing import Tuple

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from database.models import SensorData
from database.models import VehicleStatusData
from database.repository import SensorRepository
from database.repository import VehicleStatusRepository
from database.schemas import SensorType
from database.schemas import VehicleStatus


class VehicleMonitoringService:
    def __init__(self, sensor_repo: SensorRepository, vehicle_status_repo: VehicleStatusRepository):
        self.sensor_repo = sensor_repo
        self.vehicle_status_repo = vehicle_status_repo

    def register_vehicle(self, vehicle_serial: str, session: Session) -> Tuple[VehicleStatusData, bool]:
        """
        Register a new vehicle in the system with an initial status.
        Returns: (vehicle_status, created) where created is True if a new vehicle was registered
        """
        try:
            return self.vehicle_status_repo.create_vehicle(vehicle_serial, session)
        except Exception as e:
            print(f"Error registering vehicle: {e}")
            raise

    def record_sensor_data(
        self, vehicle_serial: str, sensor_type: SensorType, value: float, session: Session
    ) -> SensorData:
        # First check if vehicle exists
        try:
            self.vehicle_status_repo.get_by_serial(vehicle_serial, session)
        except NoResultFound:
            raise ValueError(f"Cannot record sensor data: Vehicle {vehicle_serial} not registered")

        sensor_data = SensorData(vehicle_serial=vehicle_serial, sensor_type=sensor_type, value=value)
        return self.sensor_repo.add(sensor_data, session)

    def get_sensor_readings(self, vehicle_serial: str, sensor_type: SensorType, session: Session) -> List[SensorData]:
        return self.sensor_repo.get_by_vehicle_and_type(vehicle_serial, sensor_type, session)

    def get_all_sensor_readings(self, vehicle_serial: str, session: Session) -> List[SensorData]:
        return self.sensor_repo.get_by_serial(vehicle_serial, session)

    def update_vehicle_status(
        self, vehicle_serial: str, new_status: VehicleStatus, session: Session
    ) -> VehicleStatusData:
        try:
            return self.vehicle_status_repo.update_status(vehicle_serial, new_status, session)
        except ValueError as e:
            print(f"Error updating vehicle status: {e}")
            raise

    def get_all_sensor_data_by_vehicle_serial(self, vehicle_serial: str, session: Session):
        try:
            all_sensor_data = self.sensor_repo.get_all_by_vehicle_serial(vehicle_serial=vehicle_serial, session=session)
        except Exception:
            print(f"Failed to get all sensor data for vehicle with serial: {vehicle_serial}")
            raise

        return all_sensor_data
