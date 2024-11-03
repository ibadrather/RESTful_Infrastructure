#include "VehicleClient.hpp"
#include "json.hpp"
#include <iostream>
#include <chrono>
#include <ctime>
#include <curl/curl.h>
#include <sstream>

using json = nlohmann::json;

namespace {

// Function to handle CURL write callback
size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

} // unnamed namespace

VehicleClient::VehicleClient(const std::string& baseUrl) : baseUrl(baseUrl) {
    curl_global_init(CURL_GLOBAL_DEFAULT);
}

VehicleClient::~VehicleClient() {
    curl_global_cleanup();
}

bool VehicleClient::addSensorData(SensorType sensorType, float sensorData, const std::string& vehicleSerial) {
    std::string timestamp = getCurrentTimestamp();
    std::string sensorTypeStr = sensorTypeToString(sensorType);

    // Format JSON payload
    std::string jsonPayload = "{"
        "\"sensor_type\": \"" + sensorTypeStr + "\","
        "\"timestamp\": \"" + timestamp + "\","
        "\"sensor_data\": " + std::to_string(sensorData) + ","
        "\"vehicle_serial\": \"" + vehicleSerial + "\""
    "}";

    return sendRequest("/add-sensor-data/", jsonPayload);
}

std::string VehicleClient::getCurrentTimestamp() const {
    using namespace std::chrono;
    auto now = system_clock::now();
    auto now_time_t = system_clock::to_time_t(now);
    auto now_us = duration_cast<microseconds>(now.time_since_epoch()) % 1000000;

    std::ostringstream oss;
    oss << std::put_time(std::gmtime(&now_time_t), "%Y-%m-%dT%H:%M:%S")
        << '.' << std::setfill('0') << std::setw(6) << now_us.count() << 'Z';

    return oss.str();
}


bool VehicleClient::sendRequest(const std::string& endpoint, const std::string& jsonPayload) {
    CURL* curl = curl_easy_init();
    if (!curl) {
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

    if (res != CURLE_OK) {
        std::cerr << "Request failed: " << curl_easy_strerror(res) << std::endl;
    } else {
        try {
            // Parse the response JSON
            auto responseJson = json::parse(responseString);

            if (responseJson.contains("status") && responseJson["status"] == "success") {
                std::cout << "Success: " << responseJson["message"] << std::endl;
                success = true;
            } else if (responseJson.contains("detail")) {
                std::cerr << "Error: " << responseJson["detail"] << std::endl;
            } else {
                std::cerr << "Unexpected response: " << responseString << std::endl;
            }
        } catch (json::parse_error& e) {
            std::cerr << "Failed to parse JSON response: " << e.what() << std::endl;
            std::cerr << "Raw response: " << responseString << std::endl;
        }
    }

    // Clean up
    curl_easy_cleanup(curl);
    curl_slist_free_all(headers);

    return success;
}

std::pair<bool, std::string> VehicleClient::getVehicleStatus(const std::string& vehicleSerial) {
    CURL* curl = curl_easy_init();
    if (!curl) {
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

    if (res != CURLE_OK) {
        curl_easy_cleanup(curl);
        return {false, std::string("Request failed: ") + curl_easy_strerror(res)};
    }

    // Clean up CURL
    curl_easy_cleanup(curl);

    try {
        auto responseJson = json::parse(responseString);

        if (responseJson.contains("status") && responseJson["status"] == "success") {
            return {true, responseJson["message"]};
        } else if (responseJson.contains("detail")) {
            return {false, responseJson["detail"]};
        } else {
            return {false, "Unexpected response format"};
        }
    } catch (json::parse_error& e) {
        return {false, std::string("Failed to parse response: ") + e.what()};
    }
}
