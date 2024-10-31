import pendulum

from database.monitoring import VehicleMonitoringService
from database.repository import SensorRepository
from database.repository import VehicleStatusRepository
from database.schemas import SensorType
from database.schemas import VehicleStatus
from database.session import DatabaseSession


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
    monitoring_service = VehicleMonitoringService(sensor_repo, vehicle_status_repo)

    # Use the first session from the generator
    session = next(db.get_session())

    try:
        # First register the vehicle
        print("Registering vehicle ABC123...")
        monitoring_service.register_vehicle(vehicle_serial="ABC123", session=session)

        # Example usage
        monitoring_service.record_sensor_data("ABC123", SensorType.TEMPERATURE, random.uniform(25, 120), session)
        monitoring_service.record_sensor_data("ABC123", SensorType.WEIGHT, random.uniform(500, 3000), session)
        monitoring_service.record_sensor_data("ABC123", SensorType.FUEL, random.uniform(0, 100), session)

        # Update vehicle status
        monitoring_service.update_vehicle_status("ABC123", VehicleStatus.ACTIVE, session)

        # Query temperature readings
        temp_readings = monitoring_service.get_sensor_readings("ABC123", SensorType.TEMPERATURE, session)

        all_sensor_data_for_vehicle = monitoring_service.get_all_sensor_data_by_vehicle_serial("ABC123", session)
        vehicle_serial = all_sensor_data_for_vehicle["vehicle_serial"]
        for key, value in all_sensor_data_for_vehicle.items():
            if not isinstance(value, tuple):
                print(f"Vehicle Serial Number: {value}")
            else:
                print(f"Sensor type: {key}")
                print(f"Sensor timestamps: {[pendulum.parse(timestamp).timestamp() for timestamp in value[0]]}")
                print(f"Sensor data: {value[1]}")

    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()
