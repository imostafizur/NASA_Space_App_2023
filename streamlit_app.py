import streamlit as st
import requests
from datetime import datetime, timedelta
import polars as pl

# NASA API key
api_key = "zJZ8G6IJOHZWRXRTXGvR89gwzkD9gtLlnmBRMD5q"

# Define the NASA API base URL
base_url = "https://api.nasa.gov/DONKI"

# Function to make API requests
def make_api_request(service, params={}):
    params["api_key"] = api_key
    response = requests.get(f"{base_url}/{service}", params=params)
    return response.json()

# Streamlit app title
st.title("Space Weather Database Of Notifications, Knowledge, Information")

# Service selection box
selected_service = st.selectbox("Select a service:", ["CME Analysis", "GST", "IPS", "FLR", "SEP", "MPC", "RBE", "HSS"])

# Date selection
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=30)
start_date = st.date_input("Start Date", start_date)
end_date = st.date_input("End Date", end_date)

# Parameters based on the selected service
params = {"startDate": start_date.strftime("%Y-%m-%d"), "endDate": end_date.strftime("%Y-%m-%d")}

if selected_service == "CME Analysis":
    most_accurate_only = st.checkbox("Most Accurate Only", True)
    speed = st.number_input("Minimum Speed (km/s)", 0)
    half_angle = st.number_input("Minimum Half Angle (degrees)", 0)
    catalog = st.selectbox("Catalog", ["ALL", "SWRC_CATALOG", "JANG_ET_AL_CATALOG"])
    
    params.update({
        "mostAccurateOnly": most_accurate_only,
        "speed": speed,
        "halfAngle": half_angle,
        "catalog": catalog
    })

# Button to fetch data
if st.button("Fetch Data"):
    with st.spinner("Fetching data..."):
        if selected_service == "CME Analysis":
            data = make_api_request("CMEAnalysis", params)
        elif selected_service == "GST":
            data = make_api_request("GST", params)
        elif selected_service == "IPS":
            location = st.selectbox("Location", ["ALL", "Earth", "MESSENGER", "STEREO A", "STEREO B"])
            catalog = st.selectbox("Catalog", ["SWRC_CATALOG", "WINSLOW_MESSENGER_ICME_CATALOG"])
            params.update({"location": location, "catalog": catalog})
            data = make_api_request("IPS", params)
        elif selected_service == "FLR":
            data = make_api_request("FLR", params)
        elif selected_service == "SEP":
            data = make_api_request("SEP", params)
        elif selected_service == "MPC":
            data = make_api_request("MPC", params)
        elif selected_service == "RBE":
            data = make_api_request("RBE", params)
        elif selected_service == "HSS":
            data = make_api_request("HSS", params)

    # Display the retrieved data in a Polars DataFrame
    if data:
        # Check if the data is a list of dictionaries (rows of data)
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            # Create a Polars DataFrame
            df = pl.DataFrame(data)
            st.write("Data Retrieved:")
            st.write(df)
        else:
            st.write("No valid data retrieved.")
    else:
        st.write("No data retrieved.")
