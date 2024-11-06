# API Documentation

This API, built with FastAPI, is designed to manage vehicle and sensor data in a backend infrastructure. Below is the documentation that details the functionality and endpoints, as well as an explanation of the choice of FastAPI.

### Recommended

For interactive documentation with SwaggerUI use the following link. You can also use the API via this interface.

[Access API Documentation here](https://restful-infrastructure.onrender.com/docs)

### Why FastAPI?

FastAPI was chosen for its performance and ease of use. It offers automatic OpenAPI and JSON schema generation, making it simple to create interactive documentation and improving developer experience. FastAPI’s asynchronous capabilities and dependency injection are also well-suited for building APIs with database connections, making it ideal for handling vehicle data in real time.

---

### API Endpoints

#### Base URL

- `/` — **Redirects to the Swagger UI documentation** .

---

### Vehicle Management Endpoints

1. **Register a New Vehicle**
  - **Endpoint:**  `/register-new-vehicle/`

  - **Method:**  `POST`

  - **Description:**  Registers a new vehicle using a unique serial number.

  - **Parameters:**
    - `vehicle_serial` (string, required): Serial number of the vehicle.

  - **Responses:**
    - `200 OK`: Vehicle registered successfully.

    - `400 Bad Request`: If registration fails.

---

2. **Update Vehicle Status**
  - **Endpoint:**  `/update-vehicle-status/`

  - **Method:**  `POST`

  - **Description:**  Updates the operational status of a registered vehicle.

  - **Body:**  Accepts `VehicleStatusData` schema containing:
    - `vehicle_serial` (string, required): Serial number of the vehicle.

    - `vehicle_status` (enum, required): The updated status of the vehicle.

  - **Responses:**
    - `200 OK`: Status updated successfully.

    - `400 Bad Request`: If the update fails.

---

3. **Retrieve All Registered Vehicles**
  - **Endpoint:**  `/get-all-vehicles`

  - **Method:**  `GET`

  - **Description:**  Returns a list of all registered vehicle serial numbers.

  - **Responses:**
    - `200 OK`: List of vehicle serial numbers.

    - `400 Bad Request`: If retrieval fails.

---

4. **Get Vehicle Status**
  - **Endpoint:**  `/get-vehicle-status/`

  - **Method:**  `GET`

  - **Description:**  Retrieves the current status of a specified vehicle.

  - **Parameters:**
    - `vehicle_serial` (string, required): Serial number of the vehicle.

  - **Responses:**
    - `200 OK`: Status of the vehicle.

    - `400 Bad Request`: If retrieval fails.

---

### Sensor Data Management Endpoints

1. **Record Sensor Data**
  - **Endpoint:**  `/add-sensor-data/`

  - **Method:**  `POST`

  - **Description:**  Records sensor data for a specified vehicle.

  - **Body:**  Accepts `SensorData` schema containing:
    - `vehicle_serial` (string, required): Serial number of the vehicle.

    - `sensor_type` (enum, required): Type of sensor (e.g., temperature, speed).

    - `sensor_data` (string, required): Data collected from the sensor.

    - `timestamp` (datetime, required): Timestamp of the data collection.

  - **Responses:**
    - `200 OK`: Sensor data recorded successfully.

    - `400 Bad Request`: If recording fails.

---

2. **Get All Sensor Data for a Vehicle**
  - **Endpoint:**  `/get-sensor-data/{vehicle_serial}`

  - **Method:**  `GET`

  - **Description:**  Retrieves all recorded sensor data for a specified vehicle.

  - **Parameters:**
    - `vehicle_serial` (string, required): Serial number of the vehicle.

  - **Responses:**
    - `200 OK`: List of all sensor data.

    - `404 Not Found`: If data retrieval fails.

---

3. **Get Specific Sensor Data by Type**
  - **Endpoint:**  `/get-sensor-data/{vehicle_serial}/{sensor_type}`

  - **Method:**  `GET`

  - **Description:**  Retrieves specific sensor data for a vehicle by sensor type.

  - **Parameters:**
    - `vehicle_serial` (string, required): Serial number of the vehicle.

    - `sensor_type` (enum, required): Type of sensor data to retrieve.

  - **Responses:**
    - `200 OK`: Specific sensor data retrieved.

    - `404 Not Found`: If data retrieval fails.

---
