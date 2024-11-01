from typing import Any
from typing import Dict
from typing import List

from conflog import logger
from database.datatypes import SensorType
from database.datatypes import VehicleStatus
from database.models import SensorData
from database.models import VehicleStatusData
from database.repository import SensorRepository
from database.repository import VehicleStatusRepository
from sqlalchemy.orm import Session


class VehicleDataManager:
    """Manages vehicle data in the relevent databases for vehicle registration, status updates, and sensor data records."""

    def __init__(self, sensor_data_repository: SensorRepository, vehicle_status_repository: VehicleStatusRepository):
        """Initializes VehicleDataManager with repositories for sensor data and vehicle status.

        Args:
            sensor_data_repository (SensorRepository): The repository for sensor data.
            vehicle_status_repository (VehicleStatusRepository): The repository for vehicle status data.
        """
        self.sensor_data_repository = sensor_data_repository
        self.vehicle_status_repository = vehicle_status_repository
        self.logger = logger.getChild(self.__class__.__name__)

    def register_new_vehicle_and_initialize_status(self, vehicle_serial: str, session: Session) -> bool:
        """Registers a new vehicle with an initial status.

        Args:
            vehicle_serial (str): The unique identifier for the vehicle.
            session (Session): SQLAlchemy session for database transactions.

        Returns:
            Tuple[VehicleStatusData, bool]: The vehicle status data and a boolean indicating if a new record was created.
        """
        return self.vehicle_status_repository.create_vehicle(vehicle_serial, session)

    def update_vehicle_status_by_serial_number(self, vehicle_serial: str, new_status: VehicleStatus, session: Session):
        """Updates the status of a specific vehicle.

        Args:
            vehicle_serial (str): The unique identifier for the vehicle.
            new_status (VehicleStatus): The new status to assign to the vehicle.
            session (Session): SQLAlchemy session for database transactions.

        Returns:
            VehicleStatusData: Updated vehicle status data.
        """
        return self.vehicle_status_repository.update_status_of_particular_vehicle(vehicle_serial, new_status, session)

    def record_sensor_data_for_vehicle(
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
        """
        self.logger.debug(f"Recording sensor data for vehicle {vehicle_serial} - Sensor: {sensor_type}, Value: {value}")
        # First check if vehicle exists
        self.vehicle_status_repository.get_vehicle_status(vehicle_serial, session)
        sensor_data = SensorData(vehicle_serial=vehicle_serial, sensor_type=sensor_type, value=value)

        return self.sensor_data_repository.insert_sensor_data_entry(sensor_data, session)

    def fetch_specific_sensor_data_for_vehicle(
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
        self.logger.debug(f"Fetching {sensor_type} sensor data for vehicle {vehicle_serial}")
        return self.sensor_data_repository.fetch_specific_sensor_data_for_vehicle(vehicle_serial, sensor_type, session)

    def fetch_all_sensor_data_for_vehicle(self, vehicle_serial: str, session: Session):
        """Fetches all sensor data for a specific vehicle.

        Args:
            vehicle_serial (str): The unique identifier for the vehicle.
            session (Session): SQLAlchemy session for database transactions.

        Returns:
            Dict[str, Any]: Dictionary containing organized sensor data for all sensors of the vehicle.
        """
        self.logger.debug(f"Fetching all sensor data for vehicle {vehicle_serial}")
        return self.sensor_data_repository.fetch_all_sensor_data_for_vehicle(
            vehicle_serial=vehicle_serial, session=session
        )

    def retrieve_vehicle_status(self, vehicle_serial: str, session: Session) -> VehicleStatusData:
        """Retrieves the current status of a specific vehicle.

        Args:
            vehicle_serial (str): The unique identifier for the vehicle.
            session (Session): SQLAlchemy session for database transactions.

        Returns:
            VehicleStatusData: The current status data of the vehicle.
        """
        self.logger.debug(f"Retrieving status for vehicle {vehicle_serial}")
        return self.vehicle_status_repository.get_vehicle_status(vehicle_serial, session)

    def retrieve_all_vehicle_serial_numbers(self, session: Session) -> List[str]:
        """Retrieves a list of all vehicle serial numbers in the database.

        Args:
            session (Session): SQLAlchemy session for database transactions.

        Returns:
            List[str]: List of all vehicle serial numbers.
        """
        self.logger.debug("Retrieving all vehicle serial numbers")
        return self.vehicle_status_repository.get_all_vehicles(session)
