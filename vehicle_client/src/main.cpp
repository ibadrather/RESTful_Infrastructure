#include "VehicleClient.hpp"
#include "SensorType.hpp"
#include <iostream>

int main() {
    VehicleClient client("http://0.0.0.0:8000");

    // Example usage with different sensor types
    if (client.addSensorData(SensorType::TEMPERATURE, 93.5, "cpp_tc")) {
        std::cout << "Temperature data sent successfully!" << std::endl;
    }

    if (client.addSensorData(SensorType::FUEL, 75.0, "DEF456")) {
        std::cout << "Fuel level data sent successfully!" << std::endl;
    }

    if (client.addSensorData(SensorType::WEIGHT, 700.0, "cpp_tc")) {
        std::cout << "Fuel level data sent successfully!" << std::endl;
    }

    return 0;
}
