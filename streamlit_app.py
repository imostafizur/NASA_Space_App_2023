import streamlit as st
import requests
from datetime import datetime, timedelta

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
st.title("Space Weather Database Of Notifications, Knowledge, Information (DONKI) Tool for Solar Events Tracking and Analysis")

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

    # Display the retrieved data
    st.write("Data Retrieved:")
    st.write(data)

# Button to display documentation
if st.button("Documentation"):
    
    st.image("phenomena_header.png", use_column_width=True)
    st.markdown("## Space Weather Software for Solar Events Tracking Using DONKI") 
    
    st.markdown("### Overview")
    st.markdown("Currently, there is no central database for space weather researchers and forecasters to ascertain observed space weather events. Instead, data is being recorded by scientists in a blog. However, this information is not easily searchable. This innovation is a database where weather events are entered and linkages, relationships, and cause-and-effects between various space weather events are recorded.")
    
    st.markdown("### The Technology")
    st.markdown("The Space Weather DONKI builds a catalog of past, present, ongoing, and expected Space Weather events. The catalog contains both forecaster logs and notifications. DONKI version 2.0 of has a comprehensive web-service API access for users to obtain space weather events stored in the database. The database consists of a backend and a web application. The database uses a framework that allows modularization of code and promotes code reuse. DONKI is the first application to allow space weather scientists to store all space weather events in one centralized data center. The comprehensive database provides search capability to support scientists allowing them to look into linkages, relationships, and cause-and-effects between space weather activities.")
    
    st.markdown("### Service Details")
    
    st.markdown("#### Coronal Mass Ejection (CME)")
    st.markdown("Coronal Mass Ejection (CME) data provides information about solar events where large amounts of solar materials and magnetic fields are ejected from the solar corona.")
    
    st.markdown("#### Coronal Mass Ejection (CME) Analysis")
    st.markdown("CME Analysis allows you to analyze Coronal Mass Ejection events. You can filter by accuracy, speed, half angle, and catalog.")
    
    st.markdown("#### Geomagnetic Storm (GST)")
    st.markdown("Geomagnetic Storm (GST) data provides information about disturbances in Earth's magnetic field caused by solar activity.")
    
    st.markdown("#### Interplanetary Shock (IPS)")
    st.markdown("Interplanetary Shock (IPS) data provides information about shocks and changes in the solar wind as it travels through space.")
    
    st.markdown("#### Solar Flare (FLR)")
    st.markdown("Solar Flare (FLR) data provides information about intense bursts of energy and light from the sun's surface.")
    
    st.markdown("#### Solar Energetic Particle (SEP)")
    st.markdown("Solar Energetic Particle (SEP) data provides information about high-energy particles emitted by the sun.")
    
    st.markdown("#### Magnetopause Crossing (MPC)")
    st.markdown("Magnetopause Crossing (MPC) data provides information about the crossing of Earth's magnetopause by solar wind.")
    
    st.markdown("#### Radiation Belt Enhancement (RBE)")
    st.markdown("Radiation Belt Enhancement (RBE) data provides information about enhancements in the radiation belts surrounding Earth.")
    
    st.markdown("#### High-Speed Stream (HSS)")
    st.markdown("High-Speed Stream (HSS) data provides information about high-speed solar wind streams from the sun.")
