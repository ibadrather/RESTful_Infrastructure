from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import Generic
from typing import List
from typing import TypeVar

import pendulum
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from database.models import SensorData
from database.models import VehicleStatusData
from database.schemas import SensorType
from database.schemas import VehicleStatus

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    @abstractmethod
    def add(self, item: T, session: Session) -> T:
        pass

    @abstractmethod
    def get_by_serial(self, serial: str, session: Session) -> T:
        pass


class SensorRepository(Repository[SensorData]):
    def add(self, item: SensorData, session: Session) -> SensorData:
        session.add(item)
        session.commit()
        return item

    def get_by_serial(self, vehicle_serial: str, session: Session) -> List[SensorData]:
        return session.query(SensorData).filter_by(vehicle_serial=vehicle_serial).all()

    def get_by_vehicle_and_type(
        self, vehicle_serial: str, sensor_type: SensorType, session: Session
    ) -> List[SensorData]:
        return session.query(SensorData).filter_by(vehicle_serial=vehicle_serial, sensor_type=sensor_type).all()

    def get_all_by_vehicle_serial(self, vehicle_serial: str, session: Session) -> Dict[str, Any]:
        """Fetch all sensor data for a specific vehicle serial as a list of dictionaries."""
        sensors = session.query(SensorData).filter_by(vehicle_serial=vehicle_serial).all()
        sensor_data: List[Dict[str, Any]] = [
            {
                "id": sensor.id,
                "vehicle_serial": sensor.vehicle_serial,
                "sensor_type": sensor.sensor_type.name,
                "value": sensor.value,
                "timestamp": sensor.timestamp.isoformat(),
            }
            for sensor in sensors
        ]

        return self._organize_vehicle_sensor_data(vehicle_serial, sensor_data)

    def _organize_vehicle_sensor_data(
        self, vehicle_serial: str, sensor_data_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        vehicle_sensor_data_dict: Dict[str, Any] = {"vehicle_serial": vehicle_serial}

        # Iterate through each sensor data entry
        for sensor_data in sensor_data_list:
            sensor_type = sensor_data["sensor_type"]
            timestamp = sensor_data["timestamp"]
            value = sensor_data["value"]

            # Initialize the vehicle entry if it doesn't exist
            if sensor_type not in vehicle_sensor_data_dict:
                vehicle_sensor_data_dict[sensor_type] = ([], [])

            vehicle_sensor_data_dict[sensor_type][0].append(timestamp)
            vehicle_sensor_data_dict[sensor_type][1].append(value)

        return vehicle_sensor_data_dict


class VehicleStatusRepository(Repository[VehicleStatusData]):
    def add(self, item: VehicleStatusData, session: Session) -> VehicleStatusData:
        session.add(item)
        session.commit()
        return item

    def get_by_serial(self, vehicle_serial: str, session: Session) -> VehicleStatusData:
        return session.query(VehicleStatusData).filter_by(vehicle_serial=vehicle_serial).one()

    def vehicle_exists(self, vehicle_serial: str, session: Session) -> bool:
        return session.query(VehicleStatusData).filter_by(vehicle_serial=vehicle_serial).first() is not None

    def create_vehicle(self, vehicle_serial: str, session: Session) -> tuple[VehicleStatusData, bool]:
        """
        Create a new vehicle entry if it doesn't exist.
        Returns: (vehicle_status, created) where created is True if a new vehicle was registered
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

    def update_status(self, vehicle_serial: str, new_status: VehicleStatus, session: Session) -> VehicleStatusData:
        try:
            vehicle_status = self.get_by_serial(vehicle_serial, session)
            vehicle_status.status = new_status
            vehicle_status.timestamp = pendulum.now("UTC")
            session.commit()
            return vehicle_status
        except NoResultFound:
            raise ValueError(f"No vehicle found with serial {vehicle_serial}")
