import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from database.datatypes import SensorType
from database.datatypes import VehicleStatus
from urllib3.exceptions import NewConnectionError

# Configure the base URL for the API
BASE_URL = "https://restful-infrastructure.onrender.com/"  # Adjust this to match your API host


# Function to register a new vehicle
def register_vehicle(vehicle_serial: str):
    """Register a new vehicle in the database."""
    try:
        response = requests.post(f"{BASE_URL}/register-new-vehicle/", params={"vehicle_serial": vehicle_serial})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Registration failed: {e}")
        return None


# Function to update vehicle status
def update_vehicle_status(vehicle_serial: str, status: VehicleStatus):
    """Update vehicle status in the database."""
    data = {"vehicle_serial": vehicle_serial, "vehicle_status": status.value}
    try:
        response = requests.post(f"{BASE_URL}/update-vehicle-status/", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Status update failed: {e}")
        return None


# Function to get vehicle status
def get_vehicle_status(vehicle_serial: str):
    """Get the status of a specific vehicle."""
    try:
        response = requests.get(f"{BASE_URL}/get-vehicle-status/", params={"vehicle_serial": vehicle_serial})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch vehicle status: {e}")
        return None


# Function to get all registered vehicles
def get_all_vehicles():
    """Get a list of all registered vehicles."""
    try:
        response = requests.get(f"{BASE_URL}/get-all-vehicles")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch vehicle list: {e}")
        return {"status": "failed", "content": "Failed to get vehicles"}


# Function to get sensor data
def get_sensor_data(vehicle_serial: str, sensor_type: SensorType = None):
    """Get sensor data for a specific vehicle and sensor type."""
    url = f"{BASE_URL}/get-sensor-data/{vehicle_serial}" + (f"/{sensor_type.value}" if sensor_type else "")

    try:
        response = requests.get(url)
        response.raise_for_status()
        print(response.json())
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch sensor data: {e}")
        return None


# Set up the Streamlit page
st.set_page_config(page_title="Vehicle Management System", layout="wide")
st.title("Vehicle Management System")


def main():
    # Create tabs for different functionalities
    tab1, tab2 = st.tabs(["Vehicle Management", "Sensor Data"])

    with tab1:
        st.header("Vehicle Management")

        # Vehicle Registration
        with st.expander("Register New Vehicle"):
            new_vehicle_serial = st.text_input(
                "Enter Vehicle Serial Number", help="Unique identifier for the new vehicle"
            )
            if st.button("Register Vehicle"):
                if new_vehicle_serial:
                    result = register_vehicle(new_vehicle_serial)
                    if result:
                        st.success(f"Vehicle {new_vehicle_serial} registered successfully!")
                else:
                    st.warning("Please enter a vehicle serial number.")

        # Update Vehicle Status
        with st.expander("Update Vehicle Status"):
            vehicles = get_all_vehicles()
            vehicle_serial = (
                st.selectbox("Select Vehicle", vehicles, help="Select a vehicle to update status")
                if vehicles
                else st.warning("No vehicles available")
            )
            new_status = st.selectbox(
                "Select New Status",
                [status for status in VehicleStatus],
                help="Choose the new status for the selected vehicle",
            )

            if st.button("Update Status"):
                if vehicle_serial:
                    result = update_vehicle_status(vehicle_serial, new_status)
                    if result:
                        st.success(f"Status updated successfully for vehicle {vehicle_serial}")
                else:
                    st.warning("Please select a vehicle to update status.")

        # View Vehicle Status
        with st.expander("View Vehicle Status"):
            if st.button("Refresh Vehicle List"):
                vehicles = get_all_vehicles()
                if vehicles:
                    status_data = [{"Vehicle": vehicle, "Status": get_vehicle_status(vehicle)} for vehicle in vehicles]
                    df = pd.DataFrame(status_data)
                    st.dataframe(df)
                else:
                    st.info("No vehicles registered")

    with tab2:
        st.header("Sensor Data")

        vehicles = get_all_vehicles()
        selected_vehicle = (
            st.selectbox("Select Vehicle for Sensor Data", vehicles, key="sensor_vehicle_select")
            if vehicles
            else st.warning("No vehicles available")
        )
        selected_sensor = st.selectbox(
            "Select Sensor Type",
            [None] + [sensor for sensor in SensorType],
            format_func=lambda x: "All Sensors" if x is None else x.name.capitalize(),
            help="Choose sensor data type to view",
        )

        if st.button("Fetch Sensor Data"):
            if selected_vehicle:
                sensor_data = get_sensor_data(selected_vehicle, selected_sensor)
                if sensor_data and isinstance(sensor_data, list):
                    df = pd.DataFrame(sensor_data)
                    df["timestamp"] = pd.to_datetime(df["timestamp"])

                    # Interactive plot
                    fig = px.line(
                        df,
                        x="timestamp",
                        y="value",
                        color="sensor_type" if "sensor_type" in df.columns else None,
                        title=f"Sensor Data for Vehicle {selected_vehicle}",
                    )
                    st.plotly_chart(fig)

                    with st.expander("View Raw Data"):
                        st.dataframe(df)
                else:
                    st.info("No sensor data available for this vehicle and sensor type.")

    # Footer
    st.markdown("---")
    st.markdown("Vehicle Management System - Monitoring Dashboard")


try:
    main()
except (requests.ConnectionError, NewConnectionError):
    st.error("Failed to connect to the server. Please check your connection and try again.")
except requests.RequestException as e:
    st.error(f"Failed to fetch sensor data: {e}")
