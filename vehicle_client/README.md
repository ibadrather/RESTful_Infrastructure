# Vehicle Client

## Overview

This project is a C++ client that interacts with a vehicle API to record sensor data. It is designed to handle HTTP requests for different sensor types, sending data to an API server with detailed checks on the response. This project leverages `libcurl` for HTTP communication and `json.hpp` (a JSON library) to handle JSON parsing.

## Project Structure

The project is organized into the following directories and files:


```bash
vehicle_client/
├── build/                     # Directory for compiled binaries
├── CMakeLists.txt             # CMake file for building the project
├── include/                   # Directory for header files
│   ├── VehicleClient.hpp      # Declaration of the VehicleClient class
│   ├── SensorType.hpp         # Declaration of the SensorType enum class
│   └── json.hpp               # JSON library for parsing API responses
└── src/                       # Directory for source files
    ├── VehicleClient.cpp      # Implementation of the VehicleClient class
    └── main.cpp               # Entry point of the application
```

### Key Components

1. **CMakeLists.txt**

  - This file is responsible for building the project. It specifies the project requirements, links dependencies (such as `libcurl`), and sets up the include directories.

  - To build the project, navigate to the project root and run:

```bash
cd vehicle_client
mkdir build
cd build
cmake ..
make
```

1. **include/VehicleClient.hpp**

  - Header file for the `VehicleClient` class, which provides an interface to interact with the vehicle API. It defines methods for sending sensor data to the server and processing responses.

  - Key methods in this class:
    - `addSensorData`: Sends sensor data to the server.

    - `sendRequest`: A helper method for making HTTP requests.

    - `getCurrentTimestamp`: Retrieves the current timestamp in ISO 8601 format.

3. **src/VehicleClient.cpp**

  - Contains the implementation of the `VehicleClient` class. This file defines how each method in `VehicleClient.hpp` operates, including formatting requests, sending data to the API, and parsing responses.

4. **include/SensorType.hpp**

  - Declares the `SensorType` enum class, which represents different types of sensors (e.g., `TEMPERATURE`, `WEIGHT`, `FUEL`). Each sensor type has a unique identifier that is included in requests to the server.

5. **src/main.cpp**
  - Entry point of the application. This file demonstrates how to initialize `VehicleClient`, send sensor data, and handle responses.

  - `main.cpp` can be customized to send various sensor data based on user requirements.

6. **include/json.hpp**

  - A header-only JSON library by [nlohmann/json](https://github.com/nlohmann/json) , included in the project to simplify JSON parsing and formatting. The library is used to parse the API's JSON response and check if the data was successfully recorded.

  - Including `json.hpp` makes it easier to work with JSON in C++, removing the need to manually parse strings and providing robust error handling.

## How to Run the Project

1. **Build the Project** :
  - Make sure you have `CMake` and `libcurl` installed on your system.

  - From the project root:

```bash
cd vehicle_client
mkdir build
cd build
cmake ..
make
```

2. **Run the Application** :
  - Once compiled, execute the program from the `build` directory:

```bashsh
./vehicle_client
```

## Why json.hpp Was Included

The project includes `json.hpp` to handle JSON data from the server. This library allows:
- **Parsing JSON Responses** : Simplifies checking for keys like `"status"` or `"message"` in the API response, providing structured error handling if the response doesn’t match expectations.

- **Cross-Compatibility** : It’s a single-header library with minimal dependencies, making it ideal for small projects where a full JSON library installation isn’t practical.
Using `json.hpp` helps the program parse and understand responses from the API in a way that is both efficient and reliable.

## Future Extensions

The modular structure of `VehicleClient` allows for easy extension. Additional API endpoints can be added with new methods in the `VehicleClient` class. Each endpoint can use `sendRequest` to handle requests and response parsing, making it straightforward to add new API functionalities.
