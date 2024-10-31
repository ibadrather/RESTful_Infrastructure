from typing import Dict
from typing import Any
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
    """Service for managing vehicle registration, status updates, and sensor data records.

    Attributes:
        sensor_repo (SensorRepository): Repository for managing sensor data.
        vehicle_status_repo (VehicleStatusRepository): Repository for managing vehicle status.
    """

    def __init__(self, sensor_repo: SensorRepository, vehicle_status_repo: VehicleStatusRepository):
        """Initializes VehicleMonitoringService with repositories for sensor data and vehicle status.

        Args:
            sensor_repo (SensorRepository): The repository for sensor data.
            vehicle_status_repo (VehicleStatusRepository): The repository for vehicle status data.
        """
        self.sensor_repo = sensor_repo
        self.vehicle_status_repo = vehicle_status_repo

    def register_vehicle(self, vehicle_serial: str, session: Session) -> Tuple[VehicleStatusData, bool]:
        """Registers a new vehicle with an initial status.

        Args:
            vehicle_serial (str): The unique identifier for the vehicle.
            session (Session): SQLAlchemy session for database transactions.

        Returns:
            Tuple[VehicleStatusData, bool]: The vehicle status data and a boolean indicating if a new record was created.

        Raises:
            Exception: If vehicle registration fails.
        """
        try:
            return self.vehicle_status_repo.create_vehicle(vehicle_serial, session)
        except Exception as e:
            print(f"Error registering vehicle: {e}")
            raise

    def update_status_of_particular_vehicle(
        self, vehicle_serial: str, new_status: VehicleStatus, session: Session
    ) -> VehicleStatusData:
        """Updates the status of a specific vehicle.

        Args:
            vehicle_serial (str): The unique identifier for the vehicle.
            new_status (VehicleStatus): The new status to assign to the vehicle.
            session (Session): SQLAlchemy session for database transactions.

        Returns:
            VehicleStatusData: Updated vehicle status data.

        Raises:
            ValueError: If the vehicle is not found.
        """
        try:
            return self.vehicle_status_repo.update_status_of_particular_vehicle(vehicle_serial, new_status, session)
        except ValueError as e:
            print(f"Error updating vehicle status: {e}")
            raise

    def record_sensor_data(
        self, vehicle_serial: str, sensor_type: SensorType, value: float, session: Session
    ) -> SensorData:
        """Records sensor data for a specific vehicle.

        Args:
            vehicle_serial (str): The unique identifier for the vehicle.
            sensor_type (SensorType): The type of sensor.
            value (float): The recorded sensor value.
            session (Session): SQLAlchemy session for database transactions.

        Returns:
            SensorData: The recorded sensor data entry.

        Raises:
            ValueError: If the vehicle is not registered.
        """
        # First check if vehicle exists
        try:
            self.vehicle_status_repo.get_by_serial(vehicle_serial, session)
        except NoResultFound:
            raise ValueError(f"Cannot record sensor data: Vehicle {vehicle_serial} not registered")

        sensor_data = SensorData(vehicle_serial=vehicle_serial, sensor_type=sensor_type, value=value)
        return self.sensor_repo.add(sensor_data, session)

    def get_particular_sensor_data_for_vehicle_with_serial_number(
        self, vehicle_serial: str, sensor_type: SensorType, session: Session
    ) -> Dict[str, Any]:
        """Fetches specific sensor data for a vehicle based on sensor type.

        Args:
            vehicle_serial (str): The unique identifier for the vehicle.
            sensor_type (SensorType): The type of sensor to retrieve data for.
            session (Session): SQLAlchemy session for database transactions.

        Returns:
            Dict[str, Any]: Dictionary containing organized sensor data for the specified sensor type.
        """

        return self.sensor_repo.get_particular_sensor_data_for_vehicle(vehicle_serial, sensor_type, session)

    def get_all_sensor_data_for_vehicle_serial(self, vehicle_serial: str, session: Session):
        """Fetches all sensor data for a specific vehicle.

        Args:
            vehicle_serial (str): The unique identifier for the vehicle.
            session (Session): SQLAlchemy session for database transactions.

        Returns:
            Dict[str, Any]: Dictionary containing organized sensor data for all sensors of the vehicle.

        Raises:
            Exception: If data retrieval fails.
        """

        try:
            all_sensor_data = self.sensor_repo.get_all_sensor_data_for_vehicle(
                vehicle_serial=vehicle_serial, session=session
            )
        except Exception:
            print(f"Failed to get all sensor data for vehicle with serial: {vehicle_serial}")
            raise

        return all_sensor_data
