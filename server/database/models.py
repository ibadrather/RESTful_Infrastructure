import pendulum
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

from database.schemas import SensorType
from database.schemas import VehicleStatus

Base = declarative_base()


class SensorData(Base):
    """Represents sensor data for a vehicle in the database.

    Attributes:
        id (int): The primary key of the sensor data entry.
        vehicle_serial (str): Unique identifier of the vehicle.
        sensor_type (SensorType): Type of sensor data being recorded.
        value (float): Measured value from the sensor.
        timestamp (datetime): Timestamp of the recorded data, automatically
            set to UTC on creation or update.
    """

    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True)
    vehicle_serial = Column(String, nullable=False)
    sensor_type = Column(Enum(SensorType), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=pendulum.now("UTC"), onupdate=pendulum.now("UTC"))


class VehicleStatusData(Base):
    """Represents status data of a vehicle in the database.

    Attributes:
        id (int): The primary key of the vehicle status entry.
        vehicle_serial (str): Unique identifier of the vehicle, cannot be null or duplicated.
        status (VehicleStatus): Operational status of the vehicle.
        timestamp (datetime): Timestamp of the status update, automatically
            set to UTC on creation or update.
    """

    __tablename__ = "vehicle_status_data"
    id = Column(Integer, primary_key=True)
    vehicle_serial = Column(String, nullable=False, unique=True)
    status = Column(Enum(VehicleStatus), nullable=False)
    timestamp = Column(DateTime, default=pendulum.now("UTC"), onupdate=pendulum.now("UTC"))


def create_database(database_name: str = "vehicle_data"):
    """Creates the SQLite database for storing vehicle and sensor data.

    This function initializes an SQLite database file named `vehicle_data.db`
    with the tables defined in `Base`. Each table's schema is based on the `SensorData`
    and `VehicleStatusData` classes.

    Args:
        database_name (str): Name of the database.
    """
    engine = create_engine(f"sqlite:///{database_name}.db")
    Base.metadata.create_all(engine)
