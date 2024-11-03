#ifndef VEHICLE_CLIENT_HPP
#define VEHICLE_CLIENT_HPP

#include <string>

#include "SensorType.hpp"

/**
 * @class VehicleClient
 * @brief A client for interacting with vehicle sensor data API endpoints.
 *
 * This class provides functions for sending sensor data to a remote server.
 * It manages API requests and processes server responses to ensure data
 * is correctly recorded.
 */
class VehicleClient
{
   public:
    /**
     * @brief Constructs a VehicleClient with a specified base URL for API requests.
     *
     * @param baseUrl The base URL for the vehicle API server.
     */
    VehicleClient(const std::string& baseUrl);

    /**
     * @brief Destructor for VehicleClient, cleans up any resources used by CURL.
     */
    ~VehicleClient();

    /**
     * @brief Sends sensor data to the server.
     *
     * This function constructs a JSON payload with sensor details and sends
     * it to the server. It also checks the server response to confirm if the
     * data was successfully recorded.
     *
     * @param sensorType The type of sensor (e.g., TEMPERATURE, WEIGHT, FUEL).
     * @param sensorData The sensor's data reading, as a float.
     * @param vehicleSerial The serial number of the vehicle.
     * @return True if the server confirms data was recorded successfully,
     *         false otherwise.
     */
    bool addSensorData(SensorType sensorType, float sensorData, const std::string& vehicleSerial);

    /**
     * @brief Retrieves the current status of a specific vehicle
     *
     * Makes an HTTP GET request to fetch the current status of a vehicle identified by
     * its serial number. The function handles the API response and returns the status
     * information.
     *
     * @param vehicleSerial The unique serial number of the vehicle to query
     * @return std::pair<bool, std::string> A pair containing:
     *         - bool: true if the request was successful, false otherwise
     *         - std::string: The vehicle's status if successful, error message if failed
     *
     * @throws std::runtime_error If CURL initialization fails
     *
     * Example:
     *   auto [success, status] = client.getVehicleStatus("VEH123");
     *   if (success) {
     *     std::cout << "Vehicle status: " << status << std::endl;
     *   }
     */
    std::pair<bool, std::string> getVehicleStatus(const std::string& vehicleSerial);

   private:
    std::string baseUrl;  ///< The base URL for the API server.

    /**
     * @brief Retrieves the current timestamp in ISO 8601 format.
     *
     * This function generates a string representing the current time in
     * UTC, formatted according to ISO 8601 (YYYY-MM-DDTHH:MM:SSZ).
     *
     * @return The current timestamp as a string.
     */
    std::string getCurrentTimestamp() const;

    /**
     * @brief Sends a JSON payload to a specified API endpoint.
     *
     * This function sends an HTTP POST request to the server with the
     * provided endpoint and JSON payload. It captures and checks the
     * response to ensure the request was successful.
     *
     * @param endpoint The endpoint to send the request to (relative to baseUrl).
     * @param jsonPayload The JSON data to be sent in the request body.
     * @return True if the server confirms data was recorded successfully,
     *         false otherwise.
     */
    bool sendRequest(const std::string& endpoint, const std::string& jsonPayload);
};

#endif  // VEHICLE_CLIENT_HPP
