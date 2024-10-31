from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import Generic, Union
from typing import List
from typing import TypeVar

import pendulum
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database.models import SensorData
from database.models import VehicleStatusData
from database.schemas import SensorType
from database.schemas import VehicleStatus

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    """Abstract base class for repository interfaces.

    Provides a generic structure for CRUD operations on database models.

    Methods:
        add: Abstract method to add an item to the database.
    """

    @abstractmethod
    def add(self, item: T, session: Session) -> T:
        pass


class SensorRepository(Repository[SensorData]):
    """Repository for managing SensorData entries in the database.

    Methods:
        add: Adds a SensorData entry and commits the transaction.
        get_particular_sensor_data_for_vehicle: Retrieves data for a specific sensor type on a vehicle.
        get_all_sensor_data_for_vehicle: Retrieves all sensor data for a vehicle.
    """

    def add(self, item: SensorData, session: Session) -> Union[SensorData, None]:
        """Adds a new SensorData entry to the database.

        Args:
            item (SensorData): The sensor data entry to add.
            session (Session): The SQLAlchemy session object.

        Returns:
            SensorData or None: The added sensor data entry, or None if the transaction fails.
        """
        try:
            session.add(item)
            session.commit()
            return item
        except SQLAlchemyError:
            session.rollback()
            # Log the exception
            return None

    def get_particular_sensor_data_for_vehicle(
        self, vehicle_serial: str, sensor_type: SensorType, session: Session
    ) -> Dict[str, Any]:
        """Fetches data for a specific sensor type on a vehicle.

        Args:
            vehicle_serial (str): The serial number of the vehicle.
            sensor_type (SensorType): The type of sensor data to retrieve.
            session (Session): The SQLAlchemy session object.

        Returns:
            Dict[str, Any]: Organized sensor data for the specified sensor type.
        """
        try:
            sensors = session.query(SensorData).filter_by(vehicle_serial=vehicle_serial, sensor_type=sensor_type).all()
            sensor_data = self._format_sensor_data(sensors)
            return self._organize_vehicle_sensor_data(vehicle_serial, sensor_data)
        except SQLAlchemyError:
            # Log the exception
            return {}

    def get_all_sensor_data_for_vehicle(self, vehicle_serial: str, session: Session) -> Dict[str, Any]:
        """Fetches all sensor data for a vehicle.

        Args:
            vehicle_serial (str): The serial number of the vehicle.
            session (Session): The SQLAlchemy session object.

        Returns:
            Dict[str, Any]: Organized sensor data for the vehicle.
        """

        try:
            sensors = session.query(SensorData).filter_by(vehicle_serial=vehicle_serial).all()
            sensor_data = self._format_sensor_data(sensors)
            return self._organize_vehicle_sensor_data(vehicle_serial, sensor_data)
        except SQLAlchemyError:
            # Log the exception
            return {}

    @staticmethod
    def _format_sensor_data(sensors: List[SensorData]) -> List[Dict[str, Any]]:
        """Converts SensorData objects to dictionaries.

        Args:
            sensors (List[SensorData]): List of SensorData objects.

        Returns:
            List[Dict[str, Any]]: List of dictionaries with sensor data fields.
        """
        return [
            {
                "id": sensor.id,
                "vehicle_serial": sensor.vehicle_serial,
                "sensor_type": sensor.sensor_type.name,
                "value": sensor.value,
                "timestamp": sensor.timestamp.isoformat(),
            }
            for sensor in sensors
        ]

    @staticmethod
    def _organize_vehicle_sensor_data(vehicle_serial: str, sensor_data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Organizes sensor data by type for a specific vehicle.

        Args:
            vehicle_serial (str): The serial number of the vehicle.
            sensor_data_list (List[Dict[str, Any]]): List of sensor data entries.

        Returns:
            Dict[str, Any]: Organized sensor data with timestamps and values.
        """
        organized_data: Dict[str, Any] = {"vehicle_serial": vehicle_serial}

        for sensor_data in sensor_data_list:
            sensor_type = sensor_data["sensor_type"]
            timestamp = sensor_data["timestamp"]
            value = sensor_data["value"]

            if sensor_type not in organized_data:
                organized_data[sensor_type] = ([], [])

            organized_data[sensor_type][0].append(timestamp)
            organized_data[sensor_type][1].append(value)

        return organized_data


class VehicleStatusRepository(Repository[VehicleStatusData]):
    """Repository for managing VehicleStatusData entries in the database.

    Methods:
        add: Adds a VehicleStatusData entry and commits the transaction.
        get_by_serial: Retrieves the vehicle status by serial number.
        vehicle_exists: Checks if a vehicle exists in the database.
        create_vehicle: Creates a new vehicle entry if it doesn't exist.
        update_status_of_particular_vehicle: Updates the status of a specific vehicle.
    """

    def add(self, item: VehicleStatusData, session: Session) -> VehicleStatusData:
        """Adds a new VehicleStatusData entry to the database.

        Args:
            item (VehicleStatusData): The vehicle status entry to add.
            session (Session): The SQLAlchemy session object.

        Returns:
            VehicleStatusData: The added vehicle status entry.
        """
        session.add(item)
        session.commit()
        return item

    def get_by_serial(self, vehicle_serial: str, session: Session) -> VehicleStatusData:
        """Retrieves the status of a vehicle by its serial number.

        Args:
            vehicle_serial (str): The serial number of the vehicle.
            session (Session): The SQLAlchemy session object.

        Returns:
            VehicleStatusData: The vehicle status entry.
        """

        return session.query(VehicleStatusData).filter_by(vehicle_serial=vehicle_serial).one()

    def vehicle_exists(self, vehicle_serial: str, session: Session) -> bool:
        """Checks if a vehicle exists in the database.

        Args:
            vehicle_serial (str): The serial number of the vehicle.
            session (Session): The SQLAlchemy session object.

        Returns:
            bool: True if the vehicle exists, False otherwise.
        """
        return session.query(VehicleStatusData).filter_by(vehicle_serial=vehicle_serial).first() is not None

    def create_vehicle(self, vehicle_serial: str, session: Session) -> tuple[VehicleStatusData, bool]:
        """Creates a new vehicle entry if it doesn't exist.

        Args:
            vehicle_serial (str): The serial number of the vehicle.
            session (Session): The SQLAlchemy session object.

        Returns:
            tuple[VehicleStatusData, bool]: Tuple of vehicle status entry and a boolean
            indicating if a new entry was created.
        """
        try:
            # First check if vehicle exists
            existing_vehicle = session.query(VehicleStatusData).filter_by(vehicle_serial=vehicle_serial).first()
            if existing_vehicle:
                return existing_vehicle, False

            # Create new vehicle if it doesn't exist
            vehicle_status = VehicleStatusData(
                vehicle_serial=vehicle_serial,
                status=VehicleStatus.INACTIVE,
                timestamp=pendulum.now("UTC"),
            )
            session.add(vehicle_status)
            session.commit()
            return vehicle_status, True

        except Exception:
            session.rollback()
            raise

    def update_status_of_particular_vehicle(
        self, vehicle_serial: str, new_status: VehicleStatus, session: Session
    ) -> VehicleStatusData:
        """Updates the status of a particular vehicle.

        Args:
            vehicle_serial (str): The serial number of the vehicle.
            new_status (VehicleStatus): The new status to set for the vehicle.
            session (Session): The SQLAlchemy session object.

        Returns:
            VehicleStatusData: Updated vehicle status entry.
        """
        try:
            vehicle_status = self.get_by_serial(vehicle_serial, session)
            vehicle_status.status = new_status
            vehicle_status.timestamp = pendulum.now("UTC")
            session.commit()
            return vehicle_status
        except NoResultFound:
            raise ValueError(f"No vehicle found with serial {vehicle_serial}")
