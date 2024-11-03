cmake_minimum_required(VERSION 3.10)
project(VehicleClientProject)

# Set C++17 as required
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Add include directory
include_directories(include)

# Find libcurl package
find_package(CURL REQUIRED)

# Add executable
add_executable(vehicle_client
    src/main.cpp
    src/VehicleClient.cpp
)

# Set compile options for modern C++
target_compile_features(vehicle_client PRIVATE cxx_std_17)

# Link CURL library
target_link_libraries(vehicle_client PRIVATE CURL::libcurl)
