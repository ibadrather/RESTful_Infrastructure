from typing import List

from api.schemas import SensorData
from api.schemas import VehicleStatusData
from conflog import logger
from database.datatypes import SensorType
from database.monitoring import VehicleDataManager
from database.repository import SensorRepository
from database.repository import VehicleStatusRepository
from database.session import DatabaseSession
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session


# Create child logger instance
logger = logger.getChild("API-Endpoints")

"""
**********************************
*** Database Initializations
**********************************
"""


# Dependency for database session
def get_session():
    """Dependency injection to provide a database session for FastAPI endpoints.

    Yields:
        Session: A SQLAlchemy session connected to the SQLite database.
    """
    db = DatabaseSession("sqlite:///server/vehicle_data.db")
    session = next(db.get_session())
    try:
        yield session
    finally:
        session.close()


# Create repositories and VehicleDataManager instance
sensor_repo = SensorRepository()
vehicle_status_repo = VehicleStatusRepository()
vehicle_data_manager = VehicleDataManager(sensor_repo, vehicle_status_repo)

"""
**********************************
*** Create FastAPI App
**********************************
"""
app = FastAPI(
    title="RESTful Infrastructure Backend API",
    description="""
    This is the backend API to store Vehicle Sensor and Status Data.
    You can add sensor data for various vehicles and change status their status.
    """,
    version="0.4.1",
    contact={
        "name": "Ibad Rather",
        "email": "ibad.rather.ir@gmail.com",
        "url": "https://www.linkedin.com/in/ibad-rather/",  # Optional LinkedIn or any profile link
    },
)


@app.get("/")
def home():
    """Redirect to Swagger UI.

    Returns:
        RedirectResponse: Redirects to the /docs route.
    """
    return RedirectResponse(url="/docs")


"""
**********************************
*** POST Methods
**********************************
"""


@app.post("/add-sensor-data/")
def record_sensor_data_for_vehicle(data: SensorData, session: Session = Depends(get_session)):
    """Record sensor data for a specific vehicle."""
    logger.debug(f"Recording sensor data for vehicle {data.vehicle_serial}")
    try:
        vehicle_data_manager.record_sensor_data_for_vehicle(
            data.vehicle_serial, data.sensor_type, data.sensor_data, session
        )
        return {"status": "success", "message": "Sensor data recorded."}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/register-vehicle/")
def add_new_vehicle(vehicle_serial: str, session: Session = Depends(get_session)):
    """Register a new vehicle with a unique serial number."""
    logger.debug(f"Registering new vehicle with serial number {vehicle_serial}")

    try:
        vehicle_data_manager.register_new_vehicle_and_initialize_status(vehicle_serial, session)
        logger.debug(f"Vehicle {vehicle_serial} registered successfully")
        return {
            "status": "success",
            "message": f"Registered new vehicle with serial number {vehicle_serial}.",
        }

    except Exception as e:
        logger.error(f"Vehicle registration failed: {e}")
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/vehicle-status/")
def update_vehicle_status(data: VehicleStatusData, session: Session = Depends(get_session)):
    """Update the status of a specific vehicle."""
    logger.debug(f"Updating status for vehicle {data.vehicle_serial}")
    try:
        vehicle_data_manager.update_vehicle_status_by_serial_number(data.vehicle_serial, data.vehicle_status, session)
        logger.debug(f"Status updated for vehicle {data.vehicle_serial} to {data.vehicle_status}")
        return {
            "status": "success",
            "message": f"Status updated for vehicle with serial number {data.vehicle_serial} to {data.vehicle_status.value}.",
        }

    except Exception as e:
        logger.error(f"Failed to update status: {e}")
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


"""
**********************************
*** GET Methods
**********************************
"""


@app.get("/all-vehicles")
def retrieve_all_vehicle_serial_numbers(session: Session = Depends(get_session)) -> List[str]:
    """Retrieve a list of all registered vehicles."""
    logger.debug("Fetching all registered vehicles")

    try:
        vehicles = vehicle_data_manager.retrieve_all_vehicle_serial_numbers(session)
        logger.debug("Fetched all vehicles successfully")
        return vehicles

    except Exception as e:
        logger.error(f"Failed to fetch vehicles: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/vehicle-status/")
def retrieve_vehicle_status(vehicle_serial: str, session: Session = Depends(get_session)):
    """Get the status of a specific vehicle."""
    logger.debug(f"Fetching status for vehicle {vehicle_serial}")

    try:
        vehicle_status = vehicle_data_manager.retrieve_vehicle_status(vehicle_serial, session)
        logger.debug(f"Fetched status for vehicle {vehicle_serial}")
        return {
            "status": "success",
            "message": f"Vehicle status for vehicle with serial number {vehicle_serial} is {vehicle_status.status}",
        }

    except Exception as e:
        logger.error(f"Failed to fetch vehicle status: {e}")
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/sensor-data/{vehicle_serial}/{sensor_type}")
def get_particular_sensor_data(vehicle_serial: str, sensor_type: SensorType, session: Session = Depends(get_session)):
    """Retrieve specific sensor data for a vehicle."""
    logger.debug(f"Fetching {sensor_type} sensor data for vehicle {vehicle_serial}")
    try:
        sensor_data = vehicle_data_manager.fetch_specific_sensor_data_for_vehicle(vehicle_serial, sensor_type, session)
        logger.debug(f"Fetched sensor data for vehicle {vehicle_serial}")
        return sensor_data
    except Exception as e:
        logger.error(f"Failed to fetch sensor data: {e}")
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/sensor-data/{vehicle_serial}")
def get_all_sensor_data(vehicle_serial: str, session: Session = Depends(get_session)):
    """Retrieve all sensor data for a vehicle."""
    logger.debug(f"Fetching all sensor data for vehicle {vehicle_serial}")
    try:
        all_data = vehicle_data_manager.fetch_all_sensor_data_for_vehicle(vehicle_serial, session)
        logger.debug(f"Fetched all sensor data for vehicle {vehicle_serial}")
        return all_data
    except Exception as e:
        logger.error(f"Failed to fetch all sensor data: {e}")
        raise HTTPException(status_code=404, detail=str(e))