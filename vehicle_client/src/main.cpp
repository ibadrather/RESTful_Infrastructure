#include <chrono>
#include <csignal>
#include <iostream>
#include <thread>
#include <random>

#include "DataTypes.hpp"
#include "VehicleClient.hpp"

// Global flag to control program execution
bool keepRunning = true;

// Signal handler for a graceful shutdown when interrupt signal is received
void signalHandler(int signum)
{
    std::cout << "\nInterrupt signal (" << signum << ") received. Exiting the program..."
              << std::endl;
    keepRunning = false;
}

int main()
{
    // Define API URL and vehicle serial number
    std::string apiUrl = "https://restful-infrastructure.onrender.com";
    std::string vehicleSerialNumber = "enginius1";

    // Register signal handler for catching SIGINT (Ctrl+C) to exit gracefully
    signal(SIGINT, signalHandler);

    // Initialize the VehicleClient with the API endpoint
    VehicleClient client(apiUrl);

    // Set up random number generator for temperature values between 30 and 90
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> temp_dist(30.0, 90.0);


    // A. Update vehicle status on the server
    std::cout << "\n==================================" << std::endl;
    bool status_success = client.updateVehicleStatus(vehicleSerialNumber, VehicleStatus::ACTIVE);
    if (status_success)
    {
        std::cout << "Vehicle status updated successfully!" << std::endl;
    }
    else
    {
        std::cout << "Failed to update vehicle status!" << std::endl;
    }

    // B. Continuously send sensor data and retrieve vehicle status
    while (keepRunning)
    {
        std::cout << "\n==================================" << std::endl;

        // Send temperature sensor data to the server
        // Generate a random temperature value
        double temperature = temp_dist(gen);
        bool data_sent = client.addSensorData(SensorType::TEMPERATURE, temperature, vehicleSerialNumber);
        if (data_sent)
        {
            std::cout << "Successfully sent temperature data." << std::endl;
        }
        else
        {
            std::cout << "Failed to send temperature data." << std::endl;
        }

        // Retrieve the current vehicle status using structured binding (C++17 feature)
        auto [status_retrieved, vehicle_status] = client.getVehicleStatus(vehicleSerialNumber);
        if (status_retrieved)
        {
            std::cout << "Vehicle Status: " << vehicle_status << std::endl;
        }
        else
        {
            std::cerr << "Failed to retrieve vehicle status." << std::endl;
        }

        // Pause for 10 seconds before the next iteration
        std::this_thread::sleep_for(std::chrono::seconds(10));
    }

    std::cout << "Program terminated." << std::endl;
    return 0;
}
