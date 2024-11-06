# Vehicle Client

## Overview
This project is a C++ client for sending sensor data to a vehicle API, with checks on server responses. It uses `libcurl` for HTTP requests and `json.hpp` for JSON parsing.
## Project Structure


```bash
vehicle_client/
├── build/                     # Compiled binaries
├── CMakeLists.txt             # Build configuration
├── include/                   # Header files
│   ├── VehicleClient.hpp      # VehicleClient class
│   ├── DataType.hpp           # DataType enum classes
│   └── json.hpp               # JSON library
└── src/                       # Source files
    ├── VehicleClient.cpp      # VehicleClient implementation
    └── main.cpp               # Entry point
```

## Dependencies

**Build the Project**

To sucessfuly build the project Ensure `CMake` and `libcurl` are installed or install them on Linux use the following command:

```bash
sudo apt get update
sudo apt install libcurl4-openssl-dev cmake
```

### Development Dependencies

For code formatting with `clang-format`:

```bash
sudo apt get update
sudo apt install clang-format clang-tidy cppcheck
```

To format the code run use the `Makefile` target:

```bash
make format-cpp
```

Or, run directly from root folder:

```bash
find vehicle_client/ \( -name "*.cpp" -o -name "*.hpp" \) -not -name "json.hpp" -not -path "vehicle_client/build/*" -exec clang-format -i {} +
```

## How to Run the Project

Run the following commands from the root directory to compile:


```bash
cd vehicle_client
mkdir build
cd build
cmake ..
make
```

  - Or, use the `Makefile` target to both build and run the program:


```bash
make build-run-client-scratch
```

**Run the Application**
  - Execute the program from the `build` directory:

```bash
./vehicle_client
```


## How It Works

In `main.cpp`, the application continuously sends sensor data to the API and retrieves the vehicle’s status. The flow is as follows:

1. **Initialize the Client** : Set up `VehicleClient` with the API URL.

2. **Send Status Update** : Update the vehicle's status to active.

3. **Continuous Data Sending** :

  - Every 10 seconds, send temperature data and retrieve the latest status.

  - Handle a graceful shutdown upon receiving a SIGINT signal when ctrl+c is pressed.
