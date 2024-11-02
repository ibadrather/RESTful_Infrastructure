cmake_minimum_required(VERSION 3.10)
project(VehicleClientProject)

set(CMAKE_CXX_STANDARD 11)

# Add include directory
include_directories(include)

# Find libcurl package
find_package(CURL REQUIRED)

# Add executable
add_executable(vehicle_client src/main.cpp src/VehicleClient.cpp)

# Link CURL library
target_link_libraries(vehicle_client CURL::libcurl)
