#include <iostream>
#include <string>
#include <curl/curl.h>

// Function to perform POST request
bool sendSensorData(const std::string& jsonPayload) {
    CURL* curl;
    CURLcode res;

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "http://0.0.0.0:8000/add-sensor-data/");

        // Set the content type to JSON
        struct curl_slist* headers = nullptr;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // Specify the POST data
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonPayload.c_str());

        // Perform the request
        res = curl_easy_perform(curl);

        if(res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
            curl_easy_cleanup(curl);
            return false;
        }
        // Clean up
        curl_easy_cleanup(curl);
        curl_global_cleanup();
        return true;
    }
    return false;
}

int main() {
    std::string sensorDataJson = R"({
        "sensor_type": "temperature",
        "timestamp": "2024-11-02T12:00:00Z",
        "sensor_data": 23.5,
        "vehicle_serial": "cpp_tc"
    })";

    if(sendSensorData(sensorDataJson)) {
        std::cout << "Data sent successfully!" << std::endl;
    } else {
        std::cout << "Failed to send data." << std::endl;
    }

    return 0;
}
