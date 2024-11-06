# Database and Models Documentation

This application uses a database to store vehicle-related data, specifically sensor data and vehicle status data. SQLAlchemy and SQLite are chosen to implement the database and ORM (Object Relational Mapping) structure, ensuring efficient and flexible interactions with the database while keeping the setup lightweight and straightforward.

### Database

1. **SQLite** : SQLite is a lightweight, file-based relational database that requires minimal setup and configuration. It’s an ideal choice for this project, as it provides sufficient capabilities to store and retrieve data without requiring a full database server. SQLite is particularly suitable for development and small- to medium-scale applications.

2. **SQLAlchemy** : SQLAlchemy is a powerful and flexible ORM for Python, allowing us to interact with the database using Python classes and objects rather than writing raw SQL queries. SQLAlchemy supports a wide range of database systems (including SQLite, PostgreSQL, MySQL, etc.), making it an ideal choice for applications that may later need to scale or migrate to a different database system.

### Models
The code defines two models representing tables in the database, `SensorData` and `VehicleStatusData`, which store information about sensor readings and vehicle statuses, respectively.

1. **`SensorData` Model** :
  - **Table Name** : `sensor_data`

  - **Attributes** :
    - `id`: Primary key for the table (Integer).

    - `vehicle_serial`: A unique identifier for each vehicle (String).

    - `sensor_type`: Type of sensor, such as temperature, weight, or fuel, represented by the `SensorType` enum.

    - `value`: Numeric value recorded by the sensor (Float).

    - `timestamp`: Datetime of the sensor reading (DateTime).

  - **Purpose** : Stores data recorded from different sensors installed in vehicles.

2. **`VehicleStatusData` Model** :
  - **Table Name** : `vehicle_status_data`

  - **Attributes** :
    - `id`: Primary key for the table (Integer).

    - `vehicle_serial`: A unique identifier for each vehicle (String, unique constraint).

    - `status`: Current status of the vehicle, represented by the `VehicleStatus` enum.

    - `timestamp`: Datetime of the status update, defaulting to the current UTC time and updating on every modification (DateTime).

  - **Purpose** : Stores the status of each vehicle, allowing us to track vehicles that are active, inactive, under maintenance, or in an error state.

### Enums

Enums are used to define fixed sets of values for specific columns in the database:

1. **`SensorType`** : Represents possible types of sensors (Temperature, Weight, Fuel).

2. **`VehicleStatus`** : Represents possible vehicle statuses (Active, Inactive, Maintenance, Error).

Enums improve code readability, validation, and enforce consistency by ensuring that only predefined values are used.


### Database Creation (Not recommended)

Database needs to created only once in the begging. If you want to create a creat a database you need to run the `create_database` function in the `server/database/models.py` file.
