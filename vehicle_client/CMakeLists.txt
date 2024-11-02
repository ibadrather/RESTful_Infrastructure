cmake_minimum_required(VERSION 3.10)
project(MyCppProject)

set(CMAKE_CXX_STANDARD 11)

# Find the libcurl package
find_package(CURL REQUIRED)

# Add the main executable
add_executable(vehicle_client main.cpp)

# Link the CURL library to your project
target_link_libraries(vehicle_client CURL::libcurl)
