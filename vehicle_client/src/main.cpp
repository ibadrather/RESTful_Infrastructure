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
        // Attempt to send sensor data
        if (client.addSensorData(SensorType::TEMPERATURE, 93.5, vehicleSerialNumber)) {
            std::cout << "Temperature data sent successfully!" << std::endl;
        }

        // Fetch and print vehicle status
        // std::string status;
        // if (client.getVehicleStatus(vehicleSerialNumber, status)) {
        //     std::cout << "Vehicle Status: " << status << std::endl;
        // } else {
        //     std::cerr << "Failed to retrieve vehicle status." << std::endl;
        // }

        // Wait before repeating
        std::this_thread::sleep_for(std::chrono::seconds(5));
    }

    std::cout << "Program terminated." << std::endl;
    return 0;
}
