# Vehicle Sensor Data Repository Tests

This test suite verifies the functionality of repositories that handle vehicle sensor data and vehicle status information in a SQLite database using SQLAlchemy.

The tests cover two main repository classes:
- `SensorRepository`: Handles sensor data (temperature, fuel, etc.) from vehicles
- `VehicleStatusRepository`: Manages vehicle status information (active/inactive)

## Test Structure

### Fixtures (`conftest.py`)

The test suite uses pytest fixtures for dependency injection and test setup:

- `database_session`: Creates an isolated in-memory SQLite database for each test
- `sensor_repo`: Provides a fresh instance of SensorRepository
- `vehicle_status_repo`: Provides a fresh instance of VehicleStatusRepository

### Test Cases (`test_sensor_repositories.py`)

Tests cover core functionality including:
- Inserting and retrieving sensor data
- Checking vehicle existence
- Updating vehicle status
- Handling multiple sensor types
- Vehicle creation and duplicate prevention

## Running the Tests

```bash
# Run all tests
pytest server/tests

# Run with verbose output
pytest server/tests -v

# Run specific test file
pytest server/tests/test_sensor_repositories.py
```

## Test Design Philosophy

- Each test is isolated using function-scoped fixtures
- In-memory SQLite database ensures fast, isolated testing
- Tables are automatically created before each test and dropped after
- Clear assertions verify both direct results and persisted data

## Dependencies

Use Makefile target to install test dependencies from the root folder:

```bash
make py-dev-setup
```
---
