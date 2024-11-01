from typing import Any
from typing import Dict
from typing import List
from typing import Union

import pendulum
from conflog import logger
from database.datatypes import SensorType
from database.datatypes import VehicleStatus
from database.models import SensorData
from database.models import VehicleStatusData
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class SensorRepository:
    """Repository for managing SensorData entries in the database."""

    def __init__(self) -> None:
        self.logger = logger.getChild(self.__class__.__name__)

    def insert_sensor_data_entry(self, item: SensorData, session: Session) -> Union[SensorData, None]:
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
            raise ValueError("Failed to add sensor data.")

    def fetch_specific_sensor_data_for_vehicle(
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
            sensor_data = self._transform_sensor_data_to_dicts(sensors)

            if len(sensor_data) == 0:
                raise NoResultFound

            return self._group_sensor_data_by_type(vehicle_serial, sensor_data)

        except NoResultFound:
            message = f"Cannot get {sensor_type.value} data for vehicle with serial number {vehicle_serial}"

            if not self.check_vehicle_existence(vehicle_serial, session):
                message = f"Cannot get {sensor_type.value} data for vehicle with serial number {vehicle_serial} as vehicle doesn not exist."

            raise ValueError(message)

        except SQLAlchemyError as e:
            raise ValueError(e)

    def check_vehicle_existence(self, vehicle_serial: str, session: Session) -> bool:
        """Checks if a vehicle exists in the database.

        Args:
            vehicle_serial (str): The serial number of the vehicle.
            session (Session): The SQLAlchemy session object.

        Returns:
            bool: True if the vehicle exists, False otherwise.
        """
        return session.query(VehicleStatusData).filter_by(vehicle_serial=vehicle_serial).first() is not None

    def fetch_all_sensor_data_for_vehicle(self, vehicle_serial: str, session: Session) -> Dict[str, Any]:
        """Fetches all sensor data for a vehicle.

        Args:
            vehicle_serial (str): The serial number of the vehicle.
            session (Session): The SQLAlchemy session object.

        Returns:
            Dict[str, Any]: Organized sensor data for the vehicle.
        """

        try:
            sensors = session.query(SensorData).filter_by(vehicle_serial=vehicle_serial).all()
            if len(sensors) == 0:
                raise NoResultFound
            sensor_data = self._transform_sensor_data_to_dicts(sensors)
            return self._group_sensor_data_by_type(vehicle_serial, sensor_data)

        except NoResultFound:
            message = f"Cannot get data for vehicle with serial number {vehicle_serial}"

            if not self.check_vehicle_existence(vehicle_serial, session):
                message = f"Cannot get data for vehicle with serial number {vehicle_serial} as vehicle doesn not exist."

            raise ValueError(message)

    @staticmethod
    def _transform_sensor_data_to_dicts(sensors: List[SensorData]) -> List[Dict[str, Any]]:
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
    def _group_sensor_data_by_type(vehicle_serial: str, sensor_data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
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


class VehicleStatusRepository:
    """Repository for managing VehicleStatusData entries in the database."""

    def __init__(self) -> None:
        self.logger = logger.getChild(self.__class__.__name__)

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

    def get_vehicle_status(self, vehicle_serial: str, session: Session) -> VehicleStatusData:
        """Retrieves the status of a vehicle by its serial number.

        Args:
            vehicle_serial (str): The serial number of the vehicle.
            session (Session): The SQLAlchemy session object.

        Returns:
            VehicleStatusData: The vehicle status entry.
        """

        try:
            return session.query(VehicleStatusData).filter_by(vehicle_serial=vehicle_serial).one()
        except NoResultFound:
            raise ValueError(f"Cannot get vehicle status: Vehicle {vehicle_serial} not registered")

    def check_vehicle_existence(self, vehicle_serial: str, session: Session) -> bool:
        """Checks if a vehicle exists in the database.

        Args:
            vehicle_serial (str): The serial number of the vehicle.
            session (Session): The SQLAlchemy session object.

        Returns:
            bool: True if the vehicle exists, False otherwise.
        """
        return session.query(VehicleStatusData).filter_by(vehicle_serial=vehicle_serial).first() is not None

    def create_vehicle(self, vehicle_serial: str, session: Session) -> bool:
        """Creates a new vehicle entry if it doesn't exist.

        Args:
            vehicle_serial (str): The serial number of the vehicle.
            session (Session): The SQLAlchemy session object.

        Returns:
            bool: a boolean indicating if a new entry was created.
        """
        try:
            # First check if vehicle exists
            existing_vehicle = session.query(VehicleStatusData).filter_by(vehicle_serial=vehicle_serial).first()
            if existing_vehicle:
                raise ValueError(f"Vehicle with serial number: {vehicle_serial} already exists.")

            # Create new vehicle if it doesn't exist
            vehicle_status = VehicleStatusData(
                vehicle_serial=vehicle_serial,
                status=VehicleStatus.INACTIVE,
                timestamp=pendulum.now("UTC"),
            )
            session.add(vehicle_status)
            session.commit()
            return True

        except Exception as e:
            session.rollback()
            raise e

    def update_status_of_particular_vehicle(
        self, vehicle_serial: str, new_status: VehicleStatus, session: Session
    ) -> None:
        """Updates the status of a particular vehicle.

        Args:
            vehicle_serial (str): The serial number of the vehicle.
            new_status (VehicleStatus): The new status to set for the vehicle.
            session (Session): The SQLAlchemy session object.

        Returns:
            VehicleStatusData: Updated vehicle status entry.
        """
        try:
            vehicle_status = self.get_vehicle_status(vehicle_serial, session)
            vehicle_status.status = new_status
            vehicle_status.timestamp = pendulum.now("UTC")
            session.commit()

        except NoResultFound:
            raise ValueError(f"Vehicle with serial number {vehicle_serial} not found!")

    def get_all_vehicles(self, session: Session) -> List[str]:
        vehicles = session.query(VehicleStatusData).all()
        vehicles = self._format_all_vehicle_serial_number(vehicles)
        return vehicles

    @staticmethod
    def _format_all_vehicle_serial_number(vehicles: List[VehicleStatusData]) -> List[str]:
        return [str(vehicle.vehicle_serial) for vehicle in vehicles]
