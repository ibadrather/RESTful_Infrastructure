import re
from datetime import datetime
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st
from database.datatypes import SensorType
from database.datatypes import VehicleStatus
from urllib3.exceptions import NewConnectionError

# Set up the Streamlit page
st.set_page_config(page_title="Vehicle Management System", layout="wide")
st.title("Vehicle Management System")

# API Configuration
BASE_URL = "https://restful-infrastructure.onrender.com"


def api_request(method: str, endpoint: str, **kwargs) -> Tuple[bool, Any]:
    """Generic API request handler with error management"""
    try:
        response = getattr(requests, method)(f"{BASE_URL}/{endpoint}", **kwargs)
        response.raise_for_status()
        return True, response.json()
    except requests.HTTPError:
        st.error("HTTP error: Cannot fetch data for this request.")
        return False, None
    except requests.ConnectionError:
        st.error("Connection error. Please check your network connection.")
        return False, None
    except requests.Timeout:
        st.error("Request timed out. Please try again later.")
        return False, None
    except requests.RequestException:
        st.error("An error occurred: Please contact admin")
        return False, None


def get_all_vehicles() -> Tuple[bool, Any]:
    """Get a list of all registered vehicles."""
    success, data = api_request("get", "get-all-vehicles")
    if not success:
        return False, {"status": "failed", "content": "Failed to get vehicles"}
    if not data:
        return False, {"status": "failed", "content": "No vehicle data available"}
    return True, data


def check_api_connection() -> Tuple[bool, Optional[List[str]]]:
    """Verify API connection and data availability"""
    success, vehicle_data = get_all_vehicles()

    if not success:
        st.error("Connection to backend API failed, please contact the administrator.")
        return False, None

    st.success("Connected to API and vehicle data is available.")
    return True, vehicle_data


def display_registered_vehicle_list(vehicle_data: List[str]):
    """Display registered vehicles in a downloadable format"""
    st.header("Registered Vehicle List")

    with st.expander("View and Download Vehicles", expanded=True):
        vehicle_df = pd.DataFrame(vehicle_data, columns=["Vehicle Registration Number"])
        st.dataframe(vehicle_df)  # Using st.dataframe for better interaction

        # Add download button for CSV
        st.download_button("Download as CSV", vehicle_df.to_csv(index=False), "vehicle_list.csv", "text/csv")


def update_vehicle_status(vehicle_serial: str, status: VehicleStatus) -> Tuple[bool, Any]:
    """Update vehicle status in the database."""
    return api_request(
        "post", "update-vehicle-status/", json={"vehicle_serial": vehicle_serial, "vehicle_status": status.value}
    )


def get_vehicle_status(vehicle_serial: str) -> Tuple[bool, Any]:
    """Get the status of a specific vehicle."""
    return api_request("get", "get-vehicle-status/", params={"vehicle_serial": vehicle_serial})


def register_vehicle(vehicle_serial: str) -> Tuple[bool, Any]:
    """Register a new vehicle in the database."""
    return api_request("post", "register-new-vehicle/", params={"vehicle_serial": vehicle_serial})


def display_update_vehicle_status(vehicle_data: List[str]):
    """Interface for updating vehicle status"""
    st.header("Update Vehicle Status")

    with st.expander("Update Vehicle Status", expanded=True):
        selected_vehicle = st.selectbox("Select Vehicle", vehicle_data, key="update_status_vehicle")
        selected_status = st.selectbox("New Status", list(VehicleStatus), key="update_status_value")

        if st.button("Update Status", key="update_status_button"):
            success, response = update_vehicle_status(selected_vehicle, selected_status)
            if success and response:
                st.success(response["message"])


def display_vehicle_status(vehicle_data: List[str]):
    """Interface for viewing vehicle status"""
    st.header("Vehicle Status Checker")

    with st.expander("Check Vehicle Status", expanded=True):
        selected_vehicle = st.selectbox("Select Vehicle", vehicle_data, key="check_status_vehicle")

        if st.button("Check Status", key="check_status_button"):
            success, response = get_vehicle_status(selected_vehicle)
            if success and response:
                st.success(f"Vehicle {selected_vehicle}: {response['message']}")


def display_register_vehicle():
    """Interface for registering new vehicles"""
    st.header("Vehicle Registration")

    with st.expander("Register New Vehicle", expanded=True):
        vehicle_serial = st.text_input(
            "Vehicle Serial Number",
            help="Use only letters (a-z, A-Z) and numbers (0-9)",  # Updated help text
        )

        if vehicle_serial:
            # Updated regex pattern to allow all numbers (0-9)
            if not re.fullmatch(r"^[a-zA-Z0-9]+$", vehicle_serial):
                st.error("Invalid serial! Please use only letters (a-z, A-Z) and numbers (0-9).")
            else:
                if st.button("Register Vehicle"):
                    success, response = register_vehicle(vehicle_serial)
                    if success and response:
                        st.success(f"Successfully registered vehicle: {vehicle_serial}")
                    else:
                        st.error("Registration failed. Please try again.")
        else:
            st.info("Please enter a vehicle serial number.")


def get_sensor_data(vehicle_serial: str, sensor_type: SensorType) -> Tuple[bool, Any]:
    """Update vehicle status in the database."""
    return api_request("get", f"get-sensor-data/{vehicle_serial}/{sensor_type}")


def display_sensor_data(vehicle_data: List[str]):
    """Interface for updating and visualizing vehicle sensor data."""
    st.header("Display Sensor Data")

    # Select vehicle and sensor type for data visualization
    with st.expander("Select vehicle and sensor type to visualize data", expanded=True):
        selected_vehicle = st.selectbox("Select Vehicle", vehicle_data, key="select_vehicle_for_sensor_data")
        selected_sensor = st.selectbox("Sensor Type", list(SensorType), key="sensor_type_selection")

        # Fetch and plot data if button is clicked
        if st.button("Plot Data", key="plot_data_button"):
            success, response = get_sensor_data(selected_vehicle, selected_sensor)

            if success and response:
                # Extract the timestamps and sensor readings from the response
                timestamps = response.get(str(selected_sensor).upper(), [])[0]
                readings = response.get(str(selected_sensor).upper(), [])[1]

                # Convert timestamps to datetime objects for better plotting
                times = [datetime.fromisoformat(ts) for ts in timestamps]

                # Plot the data
                fig, ax = plt.subplots(figsize=(6, 3))  # Adjust width and height as needed
                ax.plot(times, readings, marker="o", linestyle="-", color="b")

                # Format plot
                ax.set_xlabel("Time")
                ax.set_ylabel(f"{selected_sensor.name} Readings")
                ax.set_title(f"{selected_sensor.name} Data for Vehicle {selected_vehicle}")
                plt.xticks(rotation=45)

                # Display plot in Streamlit
                st.pyplot(fig)

                # Clear the plot after displaying
                plt.clf()
                plt.close(fig)  # Close the figure to free memory

            else:
                st.warning("No sensor data present")


def main():
    """Main application logic"""
    try:
        connection_available, vehicles = check_api_connection()

        if connection_available and vehicles:
            # Layout the interface in two columns
            left_col, right_col = st.columns(2)

            with left_col:
                display_registered_vehicle_list(vehicles)
                display_update_vehicle_status(vehicles)

            with right_col:
                display_register_vehicle()
                display_vehicle_status(vehicles)

            display_sensor_data(vehicle_data=vehicles)

    except (requests.ConnectionError, NewConnectionError):
        st.error("Server connection failed. Please check your connection.")
    except Exception as e:
        st.error(f"Application error: {str(e)}")


if __name__ == "__main__":
    main()
