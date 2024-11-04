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

# API Configuration
BASE_URL = "https://restful-infrastructure.onrender.com/"


def api_request(method: str, endpoint: str, **kwargs) -> Tuple[bool, Any]:
    """Generic API request handler with error management"""
    try:
        response = getattr(requests, method)(f"{BASE_URL}/{endpoint}", **kwargs)
        response.raise_for_status()
        return True, response.json()
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
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

    except (requests.ConnectionError, NewConnectionError):
        st.error("Server connection failed. Please check your connection.")
    except Exception as e:
        st.error(f"Application error: {str(e)}")


if __name__ == "__main__":
    main()
