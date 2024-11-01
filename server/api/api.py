from api.schemas import SensorData
from api.schemas import VehicleStatusData
from database.datatypes import SensorType
from database.monitoring import VehicleMonitoringService
from database.repository import SensorRepository
from database.repository import VehicleStatusRepository
from database.session import DatabaseSession
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session


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


# Dependency for database session
def get_session():
    db = DatabaseSession("sqlite:///server/vehicle_data.db")
    session = next(db.get_session())
    try:
        yield session
    finally:
        session.close()


# Create repositories and service instance
sensor_repo = SensorRepository()
vehicle_status_repo = VehicleStatusRepository()
monitoring_service = VehicleMonitoringService(sensor_repo, vehicle_status_repo)


@app.get("/")
def home():
    return RedirectResponse(url="/docs")


@app.post("/sensor-data/")
def record_sensor_data(data: SensorData, session: Session = Depends(get_session)):
    try:
        monitoring_service.record_sensor_data(data.vehicle_serial, data.sensor_type, data.sensor_data, session)
        return {"status": "success", "message": "Sensor data recorded."}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/register-vehicle/")
def add_new_vehicle(vehicle_serial: str, session: Session = Depends(get_session)):
    try:
        monitoring_service.register_vehicle(vehicle_serial, session)
        return {
            "status": "success",
            "message": f"Registered new vehicle with serial number {vehicle_serial}.",
        }

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/vehicle-status/")
def update_vehicle_status(data: VehicleStatusData, session: Session = Depends(get_session)):
    try:
        monitoring_service.update_status_of_particular_vehicle(data.vehicle_serial, data.vehicle_status, session)
        return {
            "status": "success",
            "message": f"Status updated for vehicle with serial number {data.vehicle_serial} to {data.vehicle_status.value}.",
        }

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/vehicle-status/")
def get_vehicle_status(vehicle_serial: str, session: Session = Depends(get_session)):
    try:
        vehicle_status = monitoring_service.get_vehicle_status(vehicle_serial, session)
        return {
            "status": "success",
            "message": f"Vehicle status for vehicle with serial number {vehicle_serial} is {vehicle_status.status}",
        }

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/sensor-data/{vehicle_serial}/{sensor_type}")
def get_particular_sensor_data(vehicle_serial: str, sensor_type: SensorType, session: Session = Depends(get_session)):
    try:
        sensor_data = monitoring_service.get_particular_sensor_data_for_vehicle_with_serial_number(
            vehicle_serial, sensor_type, session
        )
        return sensor_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/sensor-data/{vehicle_serial}")
def get_all_sensor_data(vehicle_serial: str, session: Session = Depends(get_session)):
    try:
        all_data = monitoring_service.get_all_sensor_data_for_vehicle_serial(vehicle_serial, session)
        return all_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
