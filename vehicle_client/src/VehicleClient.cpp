#include "VehicleClient.hpp"

#include <curl/curl.h>

#include <chrono>
#include <ctime>
#include <iostream>
#include <sstream>

#include "json.hpp"

using json = nlohmann::json;

namespace
{
// Function to handle CURL write callback
size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp)
{
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

}  // unnamed namespace

VehicleClient::VehicleClient(const std::string& baseUrl) : baseUrl(baseUrl)
{
    curl_global_init(CURL_GLOBAL_DEFAULT);
}

VehicleClient::~VehicleClient()
{
    curl_global_cleanup();
}

bool VehicleClient::addSensorData(SensorType sensorType, float sensorData,
                                  const std::string& vehicleSerial)
{
    std::string timestamp = getCurrentTimestamp();
    std::string sensorTypeStr = sensorTypeToString(sensorType);

    // Format JSON payload
    std::string jsonPayload =
        "{"
        "\"sensor_type\": \"" +
        sensorTypeStr +
        "\","
        "\"timestamp\": \"" +
        timestamp +
        "\","
        "\"sensor_data\": " +
        std::to_string(sensorData) +
        ","
        "\"vehicle_serial\": \"" +
        vehicleSerial +
        "\""
        "}";

    return sendRequest("/add-sensor-data/", jsonPayload);
}

std::string VehicleClient::getCurrentTimestamp() const
{
    using namespace std::chrono;
    auto now = system_clock::now();
    auto now_time_t = system_clock::to_time_t(now);
    auto now_us = duration_cast<microseconds>(now.time_since_epoch()) % 1000000;

    std::ostringstream oss;
    oss << std::put_time(std::gmtime(&now_time_t), "%Y-%m-%dT%H:%M:%S") << '.' << std::setfill('0')
        << std::setw(6) << now_us.count() << 'Z';

    return oss.str();
}

bool VehicleClient::sendRequest(const std::string& endpoint, const std::string& jsonPayload)
{
    CURL* curl = curl_easy_init();
    if (!curl)
    {
        std::cerr << "Failed to initialize CURL" << std::endl;
        return false;
    }

    CURLcode res;
    std::string url = baseUrl + endpoint;
    std::string responseString;

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonPayload.c_str());

    // Set the write callback to capture response data
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &responseString);

    res = curl_easy_perform(curl);
    bool success = false;

    if (res != CURLE_OK)
    {
        std::cerr << "Request failed: " << curl_easy_strerror(res) << std::endl;
    }
    else
    {
        try
        {
            // Parse the response JSON
            auto responseJson = json::parse(responseString);

            if (responseJson.contains("status") && responseJson["status"] == "success")
            {
                success = true;
            }
            else if (responseJson.contains("detail"))
            {
                std::cerr << "Error: " << responseJson["detail"] << std::endl;
            }
            else
            {
                std::cerr << "Unexpected response: " << responseString << std::endl;
            }
        }
        catch (json::parse_error& e)
        {
            std::cerr << "Failed to parse JSON response: " << e.what() << std::endl;
            std::cerr << "Raw response: " << responseString << std::endl;
        }
    }

    // Clean up
    curl_easy_cleanup(curl);
    curl_slist_free_all(headers);

    return success;
}

std::pair<bool, std::string> VehicleClient::getVehicleStatus(const std::string& vehicleSerial)
{
    CURL* curl = curl_easy_init();
    if (!curl)
    {
        throw std::runtime_error("Failed to initialize CURL");
    }

    std::string responseString;
    std::string url = baseUrl + "/get-vehicle-status/?vehicle_serial=" + vehicleSerial;

    // Configure CURL
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &responseString);

    // Perform request
    CURLcode res = curl_easy_perform(curl);

    if (res != CURLE_OK)
    {
        curl_easy_cleanup(curl);
        return {false, std::string("Request failed: ") + curl_easy_strerror(res)};
    }

    // Clean up CURL
    curl_easy_cleanup(curl);

    try
    {
        // Check if responseString is a JSON object or a simple string
        if (responseString.front() == '"' && responseString.back() == '"')
        {
            // Trim the double quotes and return the content as the vehicle status
            std::string status = responseString.substr(1, responseString.size() - 2);
            return {true, status};
        }
        else
        {
            // Parse JSON if it's not a simple string
            auto responseJson = json::parse(responseString);

            if (responseJson.contains("detail"))
            {
                return {false, responseJson["detail"].get<std::string>()};
            }
            else
            {
                return {false, "Unexpected response format"};
            }
        }
    }
    catch (json::parse_error& e)
    {
        return {false, std::string("Failed to parse response: ") + e.what()};
    }
}

bool VehicleClient::updateVehicleStatus(const std::string& vehicleSerial, VehicleStatus status)
{
    CURL* curl = curl_easy_init();
    if (!curl)
    {
        std::cerr << "Failed to initialize CURL" << std::endl;
        return false;
    }

    std::string url = baseUrl + "/update-vehicle-status/";
    std::string responseString;

    // Prepare the JSON payload
    json jsonPayload;
    jsonPayload["vehicle_serial"] = vehicleSerial;
    jsonPayload["vehicle_status"] = vehicleStatusToString(status);

    // Convert JSON payload to string
    std::string jsonPayloadStr = jsonPayload.dump();

    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");

    // Set CURL options
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonPayloadStr.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &responseString);

    // Perform the request
    CURLcode res = curl_easy_perform(curl);
    bool success = false;

    if (res == CURLE_OK)
    {
        try
        {
            // Parse the response JSON
            auto responseJson = json::parse(responseString);

            if (responseJson.contains("status") && responseJson["status"] == "success")
            {
                std::cout << "Status updated successfully: " << responseJson["content"]
                          << std::endl;
                success = true;
            }
            else if (responseJson.contains("detail"))
            {
                std::cerr << "Error: " << responseJson["detail"] << std::endl;
            }
            else
            {
                std::cerr << "Unexpected response: " << responseString << std::endl;
            }
        }
        catch (json::parse_error& e)
        {
            std::cerr << "Failed to parse JSON response: " << e.what() << std::endl;
            std::cerr << "Raw response: " << responseString << std::endl;
        }
    }
    else
    {
        std::cerr << "Request failed: " << curl_easy_strerror(res) << std::endl;
    }

    // Clean up
    curl_easy_cleanup(curl);
    curl_slist_free_all(headers);

    return success;
}
