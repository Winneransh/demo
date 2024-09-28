import streamlit as st


# Apply the custom CSS
st.set_page_config(
    page_title="Telemetry Monitoring System", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="auto"
)
def add_custom_css():
    st.markdown(
        """
        <style>
        /* Set background color to white and text color to black */
        body, .main, .stApp {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        /* Ensure all text elements are black */
        h1, h2, h3, h4, h5, h6, p, label {
            color: #000000 !important;
        }
        
        /* Align content to the left */
        .main {
            text-align: left;
        }
        
        /* Customize Streamlit sidebar */
        .sidebar .sidebar-content {
            background-color: #ffffff;
        }

        /* Set button and input field font to black */
        .stButton > button, .stTextInput > div > input, .stSelectbox > div > div {
            color: #000000;
        }

        /* Remove shadow for minimalistic design */
        .stButton, .stTextInput, .stSelectbox, .stNumberInput {
            box-shadow: none;
        }

        /* Set a specific width for dropdowns and text inputs */
        .stSelectbox, .stTextInput, .stNumberInput {
            width: 250px;  /* Adjust width here */
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
    add_custom_css()
# Dictionary containing states and their corresponding districts and stations
districts_in_states = {
    "Andhra Pradesh": {},
    "Arunachal Pradesh": {},
    "Assam": {},
    "Bihar": {},
    "Chhattisgarh": {},
    "Goa": {},
    "Gujarat": {},
    "Haryana": {},
    "Himachal Pradesh": {},
    "Jharkhand": {},
    "Karnataka": {},
    "Kerala": {},
    "Madhya Pradesh": {},
    "Maharashtra": {},
    "Manipur": {},
    "Meghalaya": {},
    "Mizoram": {},
    "Nagaland": {},
    "Odisha": {},
    "Punjab": {},
    "Rajasthan": {},
    "Sikkim": {},
    "Tamil Nadu": {},
    "Telangana": {},
    "Tripura": {},
    "Uttarakhand": {},
    "West Bengal": {},
    "Uttar Pradesh": {
        "Agra": [],
        "Aligarh": [],
        "Allahabad": [],
        "Ambedkar Nagar": ["Hasanpur Jalalpur", "Khajuri Karaudi"],  # Stations in Ambedkar Nagar
        "Amethi": [],
        "Amroha": [],
        "Auraiya": [],
        "Azamgarh": [],
        "Baghpat": [],
        "Bahraich": [],
        "Ballia": [],
        "Balrampur": [],
        "Banda": [],
        "Barabanki": [],
        "Bareilly": [],
        "Basti": [],
        "Bhadohi": [],
        "Bijnor": [],
        "Budaun": [],
        "Bulandshahr": [],
        "Chandauli": [],
        "Chitrakoot": [],
        "Deoria": [],
        "Etah": [],
        "Etawah": [],
        "Faizabad": [],
        "Farrukhabad": [],
        "Fatehpur": [],
        "Firozabad": [],
        "Gautam Buddha Nagar": [],
        "Ghaziabad": [],
        "Ghazipur": [],
        "Gonda": [],
        "Gorakhpur": [],
        "Hamirpur": [],
        "Hapur": [],
        "Hardoi": [],
        "Hathras": [],
        "Jalaun": [],
        "Jaunpur": [],
        "Jhansi": [],
        "Kannauj": [],
        "Kanpur Dehat": [],
        "Kanpur Nagar": [],
        "Kasganj": [],
        "Kaushambi": [],
        "Kheri": [],
        "Kushinagar": [],
        "Lalitpur": [],
        "Lucknow": [],
        "Maharajganj": [],
        "Mahoba": [],
        "Mainpuri": [],
        "Mathura": [],
        "Mau": [],
        "Meerut": [],
        "Mirzapur": [],
        "Moradabad": [],
        "Muzaffarnagar": [],
        "Pilibhit": [],
        "Pratapgarh": [],
        "Raebareli": [],
        "Rampur": [],
        "Saharanpur": [],
        "Sambhal": [],
        "Sant Kabir Nagar": [],
        "Shahjahanpur": [],
        "Shamli": [],
        "Shravasti": [],
        "Siddharthnagar": [],
        "Sitapur": [],
        "Sonbhadra": [],
        "Sultanpur": [],
        "Unnao": [],
        "Varanasi": [],
    }
}

# Initialize session state to store dictionary of dictionaries
if "entries" not in st.session_state:
    st.session_state.entries = {}

# Initialize session state to store last recorded water level for each station
if "previous_readings" not in st.session_state:
    st.session_state.previous_readings = {}

# Streamlit app
st.title("Water Level and Telemetry Information")

# Dropdown to select state
selected_state = st.selectbox("Select State", options=list(districts_in_states.keys()))

# Dropdown to select district if the selected state is Uttar Pradesh
if selected_state == "Uttar Pradesh":
    selected_district = st.selectbox("Select District", options=list(districts_in_states[selected_state].keys()))
else:
    selected_district = None

# Dropdown to select station if the district is Ambedkar Nagar
selected_station = None
if selected_district == "Ambedkar Nagar":
    stations = districts_in_states[selected_state][selected_district]
    selected_station = st.selectbox("Select Station", options=stations)

# Input box to enter water level
water_level = st.text_input("Enter Water Level (in meters)", value="")

# Input box to enter battery percentage of the telemetry device
battery_percentage = st.text_input("Enter Battery Percentage of Telemetry Device", value="")

# Button to add new entry
if st.button("Add New Entry"):
    # Ensure all fields are filled before adding an entry
    if selected_state and (selected_district or selected_state != "Uttar Pradesh") and water_level and battery_percentage:
        try:
            water_level = float(water_level)
            battery_percentage = float(battery_percentage)
        except ValueError:
            st.error("Please enter valid numeric values for water level and battery percentage.")
            water_level = None
            battery_percentage = None
        
        if water_level is not None and battery_percentage is not None:
            # Create a unique key for each entry based on the number of entries
            entry_id = len(st.session_state.entries) + 1

            # Store the selected state, district (if applicable), station (if applicable), water level, and battery percentage
            entry = {
                "state": selected_state,
                "water_level": water_level,
                "battery_percentage": battery_percentage
            }

            if selected_district:
                entry["district"] = selected_district

            if selected_station:
                entry["station"] = selected_station

                # Check previous reading for anomaly detection
                if selected_station in st.session_state.previous_readings:
                    previous_water_level = st.session_state.previous_readings[selected_station]
                    if previous_water_level != 0 and abs(water_level - previous_water_level) / previous_water_level > 0.5:
                        st.warning(f"Anomaly in reading! The water level change at {selected_station} differs by more than 50% from the previous reading.")
                
                # Update the previous reading for the station
                st.session_state.previous_readings[selected_station] = water_level

            # Store the entry in the session state dictionary
            st.session_state.entries[entry_id] = entry

            # Check for low battery alert
            if battery_percentage < 20:
                st.warning(f"Low battery on the telemetry device at {selected_station or 'your selected station'}.")

            # Check for no water level detected
            if water_level == 0:
                st.warning(f"No water level detected at the telemetry device of {selected_station or 'your selected station'}.")

            st.success(f"Entry {entry_id} added successfully!")
    else:
        st.error("Please fill all the fields before submitting.")

