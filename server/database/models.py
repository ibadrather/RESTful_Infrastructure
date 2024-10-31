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
    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True)
    vehicle_serial = Column(String, nullable=False)
    sensor_type = Column(Enum(SensorType), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=pendulum.now("UTC"), onupdate=pendulum.now("UTC"))


class VehicleStatusData(Base):
    __tablename__ = "vehicle_status_data"
    id = Column(Integer, primary_key=True)
    vehicle_serial = Column(String, nullable=False, unique=True)
    status = Column(Enum(VehicleStatus), nullable=False)
    timestamp = Column(DateTime, default=pendulum.now("UTC"), onupdate=pendulum.now("UTC"))


def create_database():
    # Create an SQLite database and engine
    engine = create_engine("sqlite:///vehicle_data.db")
    Base.metadata.create_all(engine)
