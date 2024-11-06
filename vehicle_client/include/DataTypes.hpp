#ifndef DATA_TYPE_HPP
#define DATA_TYPE_HPP

#include <string>

enum class SensorType
{
    TEMPERATURE,
    WEIGHT,
    FUEL

};

inline std::string sensorTypeToString(SensorType type)
{
    switch (type)
    {
        case SensorType::TEMPERATURE:
            return "temperature";
        case SensorType::WEIGHT:
            return "weight";
        case SensorType::FUEL:
            return "fuel";
        default:
            return "unknown";
    }
}

enum class VehicleStatus
{
    ACTIVE,
    INACTIVE,
    MAINTENANCE,
    ERROR
};

inline std::string vehicleStatusToString(VehicleStatus status)
{
    switch (status)
    {
        case VehicleStatus::ACTIVE:
            return "active";
        case VehicleStatus::INACTIVE:
            return "inactive";
        case VehicleStatus::MAINTENANCE:
            return "maintenance";
        case VehicleStatus::ERROR:
            return "error";
        default:
            return "unknown";
    }
}

#endif  // DATA_TYPE_HPP
