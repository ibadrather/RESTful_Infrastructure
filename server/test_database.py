import pendulum
from database.datatypes import SensorType
from database.datatypes import VehicleStatus
from database.monitoring import VehicleDataManager
from database.repository import SensorRepository
from database.repository import VehicleStatusRepository
from database.session import DatabaseSession
from sqlalchemy.orm import Session


def get_all_sensor_data_for_vehicle(vehicle_data_manager: VehicleDataManager, vehicle_serial: str, session: Session):
    """Retrieve and display all sensor data for a specific vehicle.

    Args:
        vehicle_data_manager (VehicleDataManager): Service instance for vehicle monitoring.
        vehicle_serial (str): The unique identifier of the vehicle.
        session (Session): SQLAlchemy session for database transactions.

    Returns:
        None
    """
    all_sensor_data_for_vehicle = vehicle_data_manager.fetch_all_sensor_data_for_vehicle(vehicle_serial, session)
    vehicle_serial = all_sensor_data_for_vehicle["vehicle_serial"]
    for key, value in all_sensor_data_for_vehicle.items():
        if not isinstance(value, tuple):
            print(f"Vehicle Serial Number: {value}")
        else:
            print(f"Sensor type: {key}")
            print(f"Sensor timestamps: {[pendulum.parse(timestamp).timestamp() for timestamp in value[0]]}")
            print(f"Sensor data: {value[1]}")


def get_particular_sensor_data_for_vehicle(
    vehicle_data_manager: VehicleDataManager, vehicle_serial: str, sensor_type: SensorType, session: Session
):
    """Retrieve and display sensor data of a specified type for a specific vehicle.

    Args:
        vehicle_data_manager (VehicleDataManager): Service instance for vehicle monitoring.
        vehicle_serial (str): The unique identifier of the vehicle.
        sensor_type (SensorType): Type of sensor data to retrieve.
        session (Session): SQLAlchemy session for database transactions.

    Returns:
        None
    """
    sensor_data = vehicle_data_manager.fetch_specific_sensor_data_for_vehicle(vehicle_serial, sensor_type, session)

    for key, value in sensor_data.items():
        if not isinstance(value, tuple):
            print(f"Vehicle Serial Number: {value}")
        else:
            print(f"Sensor type: {key}")
            print(f"Sensor timestamps: {[pendulum.parse(timestamp).timestamp() for timestamp in value[0]]}")
            print(f"Sensor data: {value[1]}")


if __name__ == "__main__":
    import os
    import random

    os.system("clear")

    # Initialize database session
    db = DatabaseSession("sqlite:///vehicle_data.db")

    # Create repositories
    sensor_repo = SensorRepository()
    vehicle_status_repo = VehicleStatusRepository()

    # Create service
    vehicle_data_manager = VehicleDataManager(sensor_repo, vehicle_status_repo)

    # Use the first session from the generator
    session = next(db.get_session())

    try:
        # First register the vehicle
        print("Registering vehicle ABC123...")
        vehicle_data_manager.register_new_vehicle_and_initialize_status(vehicle_serial="ABC123", session=session)

        # Example usage
        vehicle_data_manager.record_sensor_data_for_vehicle(
            "ABC123", SensorType.TEMPERATURE, random.uniform(25, 120), session
        )
        vehicle_data_manager.record_sensor_data_for_vehicle(
            "ABC123", SensorType.WEIGHT, random.uniform(500, 3000), session
        )
        vehicle_data_manager.record_sensor_data_for_vehicle("ABC123", SensorType.FUEL, random.uniform(0, 100), session)

        # Update vehicle status
        vehicle_data_manager.update_vehicle_status_by_serial_number("ABC123", VehicleStatus.ACTIVE, session)

        # Query temperature readings
        temp_readings = get_particular_sensor_data_for_vehicle(
            vehicle_data_manager, "ABC123", SensorType.TEMPERATURE, session
        )

        # Query all data for a vehicle
        # get_all_sensor_data_for_vehicle(vehicle_data_manager,"ABC123", session)

    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()
