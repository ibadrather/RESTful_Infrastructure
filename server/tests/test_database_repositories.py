import pendulum
import pytest
from database.datatypes import SensorType
from database.datatypes import VehicleStatus
from database.models import SensorData
from database.models import VehicleStatusData
from database.repository import SensorRepository
from database.repository import VehicleStatusRepository
from sqlalchemy.orm import Session


def test_insert_sensor_data_entry(sensor_repo: SensorRepository, database_session: Session):
    """Tests that sensor data can be successfully inserted and persisted in the database."""
    sensor_data = SensorData(
        vehicle_serial="V123", sensor_type=SensorType.TEMPERATURE, value=23.5, timestamp=pendulum.now("UTC")
    )
    result = sensor_repo.insert_sensor_data_entry(sensor_data, database_session)
    database_session.commit()

    assert result is not None
    assert str(result.vehicle_serial) == "V123"

    saved_data = database_session.query(SensorData).first()
    assert saved_data is not None
    assert str(saved_data.vehicle_serial) == "V123"


def test_fetch_specific_sensor_data_for_vehicle(sensor_repo: SensorRepository, database_session: Session):
    """Tests retrieval of specific sensor type data for a given vehicle."""
    timestamp = pendulum.now("UTC")
    sensor_data = SensorData(vehicle_serial="V123", sensor_type=SensorType.TEMPERATURE, value=23.5, timestamp=timestamp)
    database_session.add(sensor_data)
    database_session.commit()

    result = sensor_repo.fetch_specific_sensor_data_for_vehicle("V123", SensorType.TEMPERATURE, database_session)

    assert result["vehicle_serial"] == "V123"
    assert "TEMPERATURE" in result
    assert len(result["TEMPERATURE"][0]) == 1
    assert len(result["TEMPERATURE"][1]) == 1
    assert result["TEMPERATURE"][1][0] == 23.5


def test_check_vehicle_existence(vehicle_status_repo: VehicleStatusRepository, database_session: Session):
    """Tests the vehicle existence check functionality for both existing and non-existing vehicles."""
    vehicle_status = VehicleStatusData(
        vehicle_serial="V123", status=VehicleStatus.ACTIVE, timestamp=pendulum.now("UTC")
    )
    database_session.add(vehicle_status)
    database_session.commit()

    exists = vehicle_status_repo.check_vehicle_existence("V123", database_session)
    assert exists is True

    does_not_exist = vehicle_status_repo.check_vehicle_existence("NON_EXISTENT", database_session)
    assert does_not_exist is False


def test_update_status_of_particular_vehicle(vehicle_status_repo: VehicleStatusRepository, database_session: Session):
    """Tests updating a vehicle's status from one state to another."""
    vehicle_status = VehicleStatusData(
        vehicle_serial="V123", status=VehicleStatus.INACTIVE, timestamp=pendulum.now("UTC")
    )
    database_session.add(vehicle_status)
    database_session.commit()

    vehicle_status_repo.update_status_of_particular_vehicle("V123", VehicleStatus.ACTIVE, database_session)
    updated_vehicle = vehicle_status_repo.get_vehicle_status("V123", database_session)
    assert str(updated_vehicle.status) == VehicleStatus.ACTIVE.value


def test_fetch_all_sensor_data_for_vehicle(sensor_repo: SensorRepository, database_session: Session):
    """Tests retrieval of all sensor data types for a specific vehicle."""
    sensor_data1 = SensorData(
        vehicle_serial="V123", sensor_type=SensorType.TEMPERATURE, value=23.5, timestamp=pendulum.now("UTC")
    )
    sensor_data2 = SensorData(
        vehicle_serial="V123", sensor_type=SensorType.FUEL, value=1.2, timestamp=pendulum.now("UTC")
    )
    database_session.add_all([sensor_data1, sensor_data2])
    database_session.commit()

    result = sensor_repo.fetch_all_sensor_data_for_vehicle("V123", database_session)
    assert result["vehicle_serial"] == "V123"
    assert "TEMPERATURE" in result
    assert "FUEL" in result


def test_create_vehicle(vehicle_status_repo: VehicleStatusRepository, database_session: Session):
    """Tests vehicle creation and validates that duplicate vehicle creation raises an error."""
    created = vehicle_status_repo.create_vehicle("V456", database_session)
    assert created is True

    with pytest.raises(ValueError, match="already exists"):
        vehicle_status_repo.create_vehicle("V456", database_session)
