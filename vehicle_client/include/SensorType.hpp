#ifndef SENSOR_TYPE_HPP
#define SENSOR_TYPE_HPP

#include <string>

enum class SensorType {
    TEMPERATURE,
    WEIGHT,
    FUEL
};

inline std::string sensorTypeToString(SensorType type) {
    switch (type) {
        case SensorType::TEMPERATURE: return "temperature";
        case SensorType::WEIGHT: return "weight";
        case SensorType::FUEL: return "fuel";
        default: return "unknown";
    }
}

#endif // SENSOR_TYPE_HPP
