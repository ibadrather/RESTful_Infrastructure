import re
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple

import pandas as pd
import requests
import streamlit as st
from database.datatypes import VehicleStatus
from urllib3.exceptions import NewConnectionError

# Set up the Streamlit page
st.set_page_config(page_title="Vehicle Management System", layout="wide")
st.title("Vehicle Management System")

# Configure the base URL for the API
BASE_URL = "https://restful-infrastructure.onrender.com/"  # Adjust this to match your API host


# Function to get all registered vehicles
def get_all_vehicles() -> Tuple[bool, Any]:
    """Get a list of all registered vehicles."""
    try:
        response = requests.get(f"{BASE_URL}/get-all-vehicles")
        response.raise_for_status()
        vehicles = response.json()
        if vehicles:
            return True, vehicles
        else:
            return False, {"status": "failed", "content": "No vehicle data available"}
    except requests.RequestException:
        return False, {"status": "failed", "content": "Failed to get vehicles"}


# Function to check API connection and data availability
def check_api_connection() -> Tuple[bool, Optional[List[str]]]:
    success, vehicle_data = get_all_vehicles()
    if not success:
        st.error("Connection to backend API failed, please contact the administrator.")
        return False, None
    elif not vehicle_data:
        st.warning("No vehicle data available.")
        return False, None

    st.success("Connected to API and vehicle data is available.")
    return True, vehicle_data


def display_registered_vehicle_list(vehicle_data: List["str"]):
    st.header("Registered Vehicle List Viewer")
    # Display an expandable container for the list of vehicles
    with st.expander("View available vehicles and download as CSV", expanded=True):
        vehicle_df = pd.DataFrame(
            vehicle_data, columns=["Vehicle regristration serial number"]
        )  # Convert the vehicle data to a DataFrame

        # Display the DataFrame in the app
        st.write(vehicle_df)  # type: ignore


# Function to update vehicle status
def update_vehicle_status(vehicle_serial: str, status: VehicleStatus) -> Tuple[bool, Any]:
    """Update vehicle status in the database."""
    data = {"vehicle_serial": vehicle_serial, "vehicle_status": status.value}
    try:
        response = requests.post(f"{BASE_URL}/update-vehicle-status/", json=data)
        response.raise_for_status()
        return True, response.json()
    except requests.RequestException as e:
        st.error(f"Status update failed: {e}")
        return False, None


def display_update_vehicle_status(vehicle_data: List[str]):
    # Add a section for updating vehicle status
    st.header("Update Vehicle Status")
    with st.expander("Update status of available vehicles", expanded=True):
        selected_vehicle = st.selectbox("Select a vehicle to update", vehicle_data)
        selected_status = st.selectbox("Select new status", list(VehicleStatus))

        # Update button
        if st.button("Update Status"):
            sucess, response = update_vehicle_status(selected_vehicle, selected_status)

            if sucess and response is not None:
                st.success(response["message"])
            else:
                st.error("Couldn't update vehicle status")


def get_vehicle_status(vehicle_serial: str) -> Tuple[bool, Any]:
    """Get the status of a specific vehicle."""
    try:
        response = requests.get(f"{BASE_URL}/get-vehicle-status/", params={"vehicle_serial": vehicle_serial})
        response.raise_for_status()
        return True, response.json()
    except requests.RequestException:
        st.error("Failed to fetch vehicle status")
        return False, None


def display_vehicle_status(vehicle_data: List[str]):
    # Add a section for updating vehicle status
    st.header("Get Vehicle Status")
    with st.expander("Get status of an registered vehicle", expanded=True):
        selected_vehicle = st.selectbox("Select a vehicle to get status for", vehicle_data)

        # Update button
        if st.button("Get Status"):
            sucess, response = get_vehicle_status(selected_vehicle)

            if sucess and response is not None:
                st.success(f"Status of the vehicle with serial '{selected_vehicle}' is '{response['message']}'")
            else:
                st.error("Couldn't get vehicle status")


# Function to register a new vehicle
def register_vehicle(vehicle_serial: str) -> Tuple[bool, Any]:
    """Register a new vehicle in the database."""
    try:
        response = requests.post(f"{BASE_URL}/register-new-vehicle/", params={"vehicle_serial": vehicle_serial})
        response.raise_for_status()
        return True, response.json()
    except requests.RequestException as e:
        st.error(f"Registration failed: {e}")
        return False, None


def display_register_vehicle():
    """Section for registering a new vehicle with validation."""
    st.header("Register New Vehicle")

    with st.expander("Register a new vehicle", expanded=True):
        # Input for vehicle serial
        vehicle_serial = st.text_input("Enter vehicle serial (only a-z, 0-1 allowed):")

        # Validate input: only lowercase letters (a-z) and digits (0-1)
        if vehicle_serial and not re.fullmatch(r"^[a-z0-1A-Z]+$", vehicle_serial):
            st.error("Invalid serial! Please use only lowercase letters (a-z) and numbers (0-1).")
        else:
            # Register button
            if st.button("Register"):
                if vehicle_serial:
                    success, response = register_vehicle(vehicle_serial)

                    if success and response is not None:
                        st.success(f"Registered new vehicle with serial '{vehicle_serial}'")
                    else:
                        st.error("Couldn't register new vehicle")
                else:
                    st.error("Please enter a valid vehicle serial.")


def main():
    connection_available, all_vehicles_available = check_api_connection()

    if connection_available and all_vehicles_available:
        col1, col2 = st.columns(2)
        with col1:
            display_registered_vehicle_list(all_vehicles_available)
        with col2:
            display_register_vehicle()

        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            display_update_vehicle_status(all_vehicles_available)
        with col2:
            display_vehicle_status(all_vehicles_available)


# Main execution block
try:
    main()
except (requests.ConnectionError, NewConnectionError):
    st.error("Failed to connect to the server. Please check your connection and try again.")
except requests.RequestException as e:
    st.error(f"Failed to fetch sensor data: {e}")


# # Function to get sensor data
# def get_sensor_data(vehicle_serial: str, sensor_type: SensorType = None):
#     """Get sensor data for a specific vehicle and sensor type."""
#     url = f"{BASE_URL}/get-sensor-data/{vehicle_serial}" + (f"/{sensor_type.value}" if sensor_type else "")

#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         print(response.json())
#         return response.json()
#     except requests.RequestException as e:
#         st.error(f"Failed to fetch sensor data: {e}")
#         return None
