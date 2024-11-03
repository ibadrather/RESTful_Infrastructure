#include "VehicleClient.hpp"
#include "SensorType.hpp"
#include <iostream>
#include <thread>
#include <chrono>
#include <csignal>

bool keepRunning = true;

void signalHandler(int signum) {
    std::cout << "\nInterrupt signal (" << signum << ") received. Exiting the program..." << std::endl;
    keepRunning = false;
}

int main() {
    std::string apiUrl = "http://0.0.0.0:8000";
    std::string vehicleSerialNumber = "cpp_tc";

    // Register signal handler for graceful exit
    signal(SIGINT, signalHandler);

    VehicleClient client(apiUrl);

    while (keepRunning) {
        std::cout << "\n==================================" << std::endl;

        // Attempt to send sensor data
        if (!client.addSensorData(SensorType::TEMPERATURE, 93.5, vehicleSerialNumber)) {
            std::cout << "Sending temperature data failed!!!" << std::endl;
        }

        // Get vehicle status using C++17 structured binding
        auto [status_success, vehicle_status] = client.getVehicleStatus(vehicleSerialNumber);
        if (status_success) {  // Note: changed from status_sucess to status_success
            std::cout << "Vehicle Status: " << vehicle_status << std::endl;
        } else {
            std::cerr << "Failed to retrieve vehicle status: " << vehicle_status << std::endl;
        }

        // Wait before repeating
        std::this_thread::sleep_for(std::chrono::seconds(5));
    }

    std::cout << "Program terminated." << std::endl;
    return 0;
}
