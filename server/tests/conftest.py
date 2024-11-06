from typing import Any
from typing import Generator

import pytest
from database.models import Base
from database.repository import SensorRepository
from database.repository import VehicleStatusRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="function")
def database_session() -> Generator[Session, Any, Any]:
    """Creates an isolated in-memory SQLite database session for each test.
    Automatically handles table creation and cleanup."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def sensor_repo() -> SensorRepository:
    """Provides a fresh SensorRepository instance for each test."""
    return SensorRepository()


@pytest.fixture(scope="function")
def vehicle_status_repo() -> VehicleStatusRepository:
    """Provides a fresh VehicleStatusRepository instance for each test."""
    return VehicleStatusRepository()
