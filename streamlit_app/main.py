"""
ABIA Traffic Accident Forecaster - Modern Streamlit Application

A real-time traffic accident risk predictor with modern UI/UX.
"""

import sys
from pathlib import Path

# --- Path Setup: Add project root to system path for 'src' imports ---
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# --- Standard Library & Third-Party Imports ---
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
import nest_asyncio
import time
import pytz
from timezonefinder import TimezoneFinder

# --- Local Imports from src ---
from src.config import STATE_LIST, VEHICLE_MAP, GENDER_MAP, WEATHER_CODE_MAP
from src.models import load_model_assets, prepare_prediction_input
from src.features import get_part_of_day

# Apply the patch for asyncio (required for geopy in Streamlit)
nest_asyncio.apply()

# --- Path Constants ---
MODELS_DIR = PROJECT_ROOT / 'models'
MODEL_PATH = MODELS_DIR / 'accident_predictor_model.pkl'
COLUMNS_PATH = MODELS_DIR / 'model_columns.pkl'

# --- Weather Icons Mapping ---
WEATHER_ICONS = {
    'Clear': '☀️',
    'Mainly Clear': '🌤️',
    'Partly Cloudy': '⛅',
    'Overcast': '☁️',
    'Fog': '🌫️',
    'Depositing Rime Fog': '🌫️',
    'Light Drizzle': '🌦️',
    'Moderate Drizzle': '🌧️',
    'Dense Drizzle': '🌧️',
    'Light Freezing Drizzle': '🌨️',
    'Dense Freezing Drizzle': '🌨️',
    'Slight Rain': '🌧️',
    'Moderate Rain': '🌧️',
    'Heavy Rain': '⛈️',
    'Light Freezing Rain': '🌨️',
    'Heavy Freezing Rain': '🌨️',
    'Slight Snowfall': '🌨️',
    'Moderate Snowfall': '❄️',
    'Heavy Snowfall': '❄️',
    'Snow Grains': '❄️',
    'Slight Rain Showers': '🌦️',
    'Moderate Rain Showers': '🌧️',
    'Violent Rain Showers': '⛈️',
    'Slight Snow Showers': '🌨️',
    'Heavy Snow Showers': '❄️',
    'Thunderstorm': '⛈️',
    'Thunderstorm with Slight Hail': '⛈️',
    'Thunderstorm with Heavy Hail': '⛈️',
    'Other': '🌡️'
}

# --- Custom CSS for Modern Light Theme ---
CUSTOM_CSS = """
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* ========================================
       HEADER STYLING - Visible on light BG
       ======================================== */
    .main-header {
        color: #1e293b;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 8px;
    }
    
    /* Traffic light emoji - make it visible */
    .main-header-icon {
        font-size: 2.5rem;
        margin-right: 10px;
    }
    
    .sub-header {
        color: #475569;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 24px;
    }
    
    /* ========================================
       STATES BANNER - Bold & Readable
       ======================================== */
    .states-banner {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 12px;
        padding: 16px 24px;
        margin-bottom: 24px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .states-banner-label {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.95rem;
        margin-right: 8px;
    }
    
    .states-banner-list {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    
    /* ========================================
       SECTION HEADERS - Dark & Prominent
       ======================================== */
    .section-header {
        color: #1e293b;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 3px solid #6366f1;
        display: inline-block;
    }
    
    /* ========================================
       FORM LABELS - High Contrast
       ======================================== */
    .stSelectbox label, .stTextInput label, .stRadio label, .stCheckbox label {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Toggle label */
    .stToggle > label > div > p {
        color: #1e293b !important;
        font-weight: 500 !important;
    }
    
    /* Dropdown text visibility */
    .stSelectbox > div > div > div > div {
        color: #1e293b !important;
    }
    
    /* ========================================
       INPUT STYLING
       ======================================== */
    .stTextInput > div > div > input {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        color: #1e293b;
        padding: 12px 16px;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
    }
    
    .stSelectbox > div > div {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
    }
    
    /* ========================================
       BUTTON STYLING
       ======================================== */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
    }
    
    /* ========================================
       TIME DISPLAY CARD
       ======================================== */
    .time-display {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
    }
    
    .time-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #6366f1;
    }
    
    .time-date {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 4px;
    }
    
    /* ========================================
       RISK DISPLAY CARDS
       ======================================== */
    .risk-gauge {
        background: linear-gradient(90deg, #22c55e 0%, #eab308 50%, #ef4444 100%);
        height: 14px;
        border-radius: 7px;
        position: relative;
        margin: 20px 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .risk-indicator {
        width: 6px;
        height: 26px;
        background: #1e293b;
        border-radius: 3px;
        position: absolute;
        top: -6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        border: 2px solid #22c55e;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #fef9c3 0%, #fef08a 100%);
        border: 2px solid #eab308;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 2px solid #ef4444;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
    }
    
    .risk-score {
        font-size: 3rem;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .risk-label {
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    /* ========================================
       WEATHER CARD
       ======================================== */
    .weather-card {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        border: 2px solid #0ea5e9;
        border-radius: 12px;
        padding: 20px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    .weather-icon {
        font-size: 3rem;
    }
    
    .weather-info {
        flex: 1;
    }
    
    .weather-condition {
        font-size: 1.15rem;
        font-weight: 600;
        color: #0c4a6e;
    }
    
    .weather-temp {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0369a1;
    }
    
    .weather-wind {
        color: #0c4a6e;
        font-size: 0.95rem;
        margin-top: 4px;
    }
    
    /* ========================================
       INTERPRETATION & FACTORS CARDS
       ======================================== */
    .interpretation-card {
        padding: 14px 18px;
        background: #f8fafc;
        border-radius: 10px;
        font-size: 0.95rem;
        color: #1e293b;
        margin-top: 16px;
    }
    
    .factors-card {
        margin-top: 16px;
        padding: 16px;
        background: #f8fafc;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
    
    .factors-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 10px;
    }
    
    .factors-list {
        font-size: 0.9rem;
        color: #475569;
        line-height: 1.7;
    }
    
    /* ========================================
       MAP CONTAINER
       ======================================== */
    .map-container {
        border-radius: 12px;
        overflow: hidden;
        border: 2px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* ========================================
       DIVIDER
       ======================================== */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 28px 0;
    }
    
    /* Hide empty elements */
    .element-container:empty {
        display: none;
    }
    
    /* Markdown text - dark for readability */
    .stMarkdown p, .stMarkdown li, .stMarkdown strong {
        color: #1e293b;
    }
</style>
"""

# --- Page Configuration ---
st.set_page_config(
    page_title="RoadRisk AI",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# --- Initialize Session State ---
def init_session_state():
    defaults = {
        'suggestions': [],
        'selected_address': None,
        'lat': 0.0,
        'lon': 0.0,
        'prev_state': None,
        'last_search': '',
        'last_search_time': 0,
        'prediction_made': False,
        'prediction_result': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()


# --- Model Loading with Streamlit Caching ---
@st.cache_resource
def load_model():
    """Load the trained model and columns with Streamlit caching."""
    model, model_columns = load_model_assets(MODEL_PATH, COLUMNS_PATH)
    return model, model_columns


# --- Helper Functions ---
@st.cache_data(ttl=3600, show_spinner=False)
def get_address_suggestions(address: str, state: str) -> list:
    """Get address suggestions using Photon geocoder with Nominatim fallback."""
    if not address or len(address) < 3:
        return []
    
    # Try Photon geocoder first (Komoot, better rate limits)
    try:
        from geopy.geocoders import Photon
        geolocator = Photon(user_agent="RoadRiskAI/1.0", timeout=10)
        locations = geolocator.geocode(
            f"{address}, {state}, USA",
            exactly_one=False,
            limit=5
        )
        if locations:
            return [(loc.address, loc.latitude, loc.longitude) for loc in locations]
    except Exception:
        pass  # Try Nominatim fallback
    
    # Fallback to Nominatim with delay
    try:
        time.sleep(1.5)
        geolocator = Nominatim(
            user_agent="RoadRiskAI/1.0 (roadrisk-ai.streamlit.app)",
            timeout=15
        )
        locations = geolocator.geocode(
            f"{address}, {state}, USA",
            exactly_one=False,
            limit=5
        )
        if locations:
            return [(loc.address, loc.latitude, loc.longitude) for loc in locations]
        return []
    except GeocoderUnavailable:
        return [("GEOCODER_ERROR", 0, 0)]
    except Exception:
        return [("GEOCODER_ERROR", 0, 0)]



@st.cache_data(ttl=300, show_spinner=False)
def get_live_weather(lat: float, lon: float) -> dict:
    """Fetch current weather data from Open-Meteo API."""
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,precipitation,snowfall,weather_code,wind_speed_10m"
            f"&temperature_unit=fahrenheit&wind_speed_unit=mph"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()['current']
        return {
            'temperature_f': data['temperature_2m'],
            'temperature_c': round((data['temperature_2m'] - 32) * 5/9, 1),
            'precipitation': data['precipitation'],
            'snowfall': data['snowfall'],
            'weathercode': data['weather_code'],
            'windspeed': data['wind_speed_10m']
        }
    except Exception:
        return None


def get_risk_category(probability: float) -> tuple:
    """Get risk category and styling based on probability."""
    if probability < 0.25:
        return 'Low Risk', 'risk-low', '#22c55e'
    elif probability < 0.50:
        return 'Moderate Risk', 'risk-medium', '#eab308'
    else:
        return 'High Risk', 'risk-high', '#ef4444'


def celsius_to_fahrenheit(c: float) -> float:
    return round(c * 9/5 + 32, 1)


# --- Main App ---
def main():
    # Header - now uses dark text visible on light background
    st.markdown('<h1 class="main-header">🚦 RoadRisk AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time traffic accident risk prediction powered by AI and live weather data</p>', unsafe_allow_html=True)
    
    # Load model
    model, model_columns = load_model()
    
    if model is None or model_columns is None:
        st.error("⚠️ Model files not found. Please ensure model files are in the `models/` directory.")
        return
    
    # Supported states notice - now with purple background and WHITE text
    st.markdown(f"""
        <div class="states-banner">
            <span class="states-banner-label">📍 Currently supporting:</span>
            <span class="states-banner-list">{' • '.join(STATE_LIST)}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Main content columns
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        # Location Section
        st.markdown('<div class="section-header">📍 Location</div>', unsafe_allow_html=True)
        
        # State selection
        state_col, spacer = st.columns([1, 1])
        with state_col:
            state_input = st.selectbox(
                "State",
                STATE_LIST,
                key='state_input',
                help="Select the state for your search"
            )
        
        # Clear suggestions if state changes
        if st.session_state.prev_state != state_input:
            st.session_state.suggestions = []
            st.session_state.selected_address = None
            st.session_state.prev_state = state_input
        
        # Address input with auto-suggest
        address_input = st.text_input(
            "🔍 Search Address",
            placeholder="Start typing an address (e.g., 100 N Tryon St)",
            key='address_input',
            help="Type at least 3 characters, then click Search or wait for suggestions"
        )
        
        # Search button for manual trigger
        search_col, _ = st.columns([1, 2])
        with search_col:
            search_clicked = st.button("🔍 Search", key="search_btn", use_container_width=True)
        
        # Trigger search: either button click or auto after typing
        if search_clicked and address_input and len(address_input) >= 3:
            with st.spinner("Finding addresses..."):
                st.session_state.suggestions = get_address_suggestions(address_input, state_input)
            st.session_state.last_search = address_input
        elif (address_input and 
              len(address_input) >= 3 and 
              address_input != st.session_state.last_search):
            # Auto-suggest after typing stops
            with st.spinner("Finding addresses..."):
                st.session_state.suggestions = get_address_suggestions(address_input, state_input)
            st.session_state.last_search = address_input
        
        # Display suggestions or error
        if st.session_state.suggestions:
            # Check for geocoder error
            if len(st.session_state.suggestions) == 1 and st.session_state.suggestions[0][0] == "GEOCODER_ERROR":
                st.warning("⚠️ Address search service is temporarily unavailable. Please try again in a few seconds.")
                st.session_state.suggestions = []  # Clear error state
            else:
                st.markdown("**Select an address:**")
                for i, (address, lat, lon) in enumerate(st.session_state.suggestions):
                    # Truncate long addresses for display
                    display_addr = address[:80] + "..." if len(address) > 80 else address
                    if st.button(f"📍 {display_addr}", key=f"addr_{i}", use_container_width=True):
                        st.session_state.selected_address = address
                        st.session_state.lat = lat
                        st.session_state.lon = lon
                        st.session_state.prediction_made = False
                        st.rerun()
        
        # Show selected location
        if st.session_state.selected_address:
            # Selected address with clear button
            addr_col, clear_col = st.columns([4, 1])
            with addr_col:
                st.success(f"✅ **Selected:** {st.session_state.selected_address[:80]}...")
            with clear_col:
                if st.button("🗑️ Clear", key="clear_address", help="Clear selection and search again"):
                    st.session_state.selected_address = None
                    st.session_state.suggestions = []
                    st.session_state.prediction_made = False
                    st.session_state.last_search = ''
                    st.rerun()
            
            # Map display
            st.markdown('<div class="map-container">', unsafe_allow_html=True)
            map_data = pd.DataFrame({
                'lat': [st.session_state.lat],
                'lon': [st.session_state.lon]
            })
            st.map(map_data, zoom=15)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Vehicle & Driver Section
        st.markdown('<div class="section-header">🚗 Vehicle & Driver</div>', unsafe_allow_html=True)
        
        vehicle_type = st.selectbox(
            "Vehicle Type",
            list(VEHICLE_MAP.keys()),
            key='vehicle_type'
        )
        
        gender = st.selectbox(
            "Driver Gender",
            list(GENDER_MAP.keys()),
            key='gender'
        )
        
        # Time Section
        st.markdown('<div class="section-header">🕐 Time Settings</div>', unsafe_allow_html=True)
        
        use_current_time = st.toggle("Use current time", value=True, key='use_current_time')
        
        if use_current_time:
            # Get timezone based on selected location, or default to EST
            try:
                if st.session_state.lat and st.session_state.lon:
                    tf = TimezoneFinder()
                    tz_name = tf.timezone_at(lat=st.session_state.lat, lng=st.session_state.lon)
                    if tz_name:
                        local_tz = pytz.timezone(tz_name)
                    else:
                        local_tz = pytz.timezone('America/New_York')  # Default to EST
                else:
                    local_tz = pytz.timezone('America/New_York')  # Default to EST
            except:
                local_tz = pytz.timezone('America/New_York')  # Fallback to EST
            
            now = datetime.now(local_tz)
            current_hour = now.hour
            current_part = get_part_of_day(current_hour)
            st.markdown(f"""
                <div class="time-display">
                    <div class="time-value">{now.strftime('%I:%M %p')} • {current_part}</div>
                    <div class="time-date">{now.strftime('%A, %B %d, %Y')}</div>
                </div>
            """, unsafe_allow_html=True)
            selected_part_of_day = current_part
            selected_hour = current_hour
        else:
            selected_part_of_day = st.selectbox(
                "Select Time of Day",
                ['Morning', 'Afternoon', 'Evening', 'Night'],
                key='manual_part_of_day',
                help="Morning: 5AM-12PM, Afternoon: 12PM-5PM, Evening: 5PM-9PM, Night: 9PM-5AM"
            )
            # Map part of day to representative hour
            hour_map = {'Morning': 9, 'Afternoon': 14, 'Evening': 19, 'Night': 23}
            selected_hour = hour_map[selected_part_of_day]
    
    st.markdown("---")
    
    # Prediction Button
    predict_disabled = not st.session_state.selected_address
    
    if st.button(
        "🔮 Predict Accident Risk",
        use_container_width=True,
        type="primary",
        disabled=predict_disabled
    ):
        if not st.session_state.selected_address:
            st.error("Please select an address first.")
        else:
            # Fetch weather and make prediction
            with st.status("Analyzing risk...", expanded=True) as status:
                st.write("📍 Confirming location...")
                time.sleep(0.3)
                
                st.write("🌤️ Fetching live weather data...")
                weather = get_live_weather(st.session_state.lat, st.session_state.lon)
                
                if not weather:
                    status.update(label="Error", state="error")
                    st.error("Could not fetch weather data. Please try again.")
                    return
                
                st.write("🧠 Running prediction model...")
                
                # Build input data
                now = datetime.now()
                input_data = {
                    "State": state_input,
                    "VehicleType": VEHICLE_MAP[vehicle_type],
                    "Gender": GENDER_MAP[gender],
                    "temperature": weather['temperature_c'],
                    "precipitation": weather['precipitation'],
                    "snowfall": weather['snowfall'],
                    "windspeed": weather['windspeed'] * 1.60934  # Convert mph to km/h for model
                }
                input_df = pd.DataFrame([input_data])
                
                # Add time features
                input_df['Hour'] = selected_hour
                input_df['DayOfWeek'] = now.strftime('%A')
                input_df['Month'] = now.month
                input_df['PartOfDay'] = selected_part_of_day
                
                # Add weather condition
                weather_condition = WEATHER_CODE_MAP.get(weather['weathercode'], 'Other')
                input_df['WeatherCondition'] = weather_condition
                
                # Make prediction
                final_df = prepare_prediction_input(input_df, model_columns)
                prediction = model.predict(final_df)[0]
                probability = model.predict_proba(final_df)[0][1]
                
                status.update(label="Analysis complete!", state="complete")
                
                # Store results
                st.session_state.prediction_made = True
                st.session_state.prediction_result = {
                    'prediction': prediction,
                    'probability': probability,
                    'weather': weather,
                    'weather_condition': weather_condition
                }
    
    # Display Results
    if st.session_state.prediction_made and st.session_state.prediction_result:
        result = st.session_state.prediction_result
        probability = result['probability']
        weather = result['weather']
        weather_condition = result['weather_condition']
        
        st.markdown("---")
        st.markdown('<div class="section-header">📊 Risk Assessment</div>', unsafe_allow_html=True)
        
        # Results columns
        res_col1, res_col2 = st.columns([1, 1])
        
        with res_col1:
            # Risk Gauge
            risk_label, risk_class, risk_color = get_risk_category(probability)
            indicator_pos = min(probability * 100, 100)
            
            st.markdown(f"""
                <div class="{risk_class}">
                    <div class="risk-label" style="color: {risk_color};">{risk_label}</div>
                    <div class="risk-score" style="color: {risk_color};">{probability:.1%}</div>
                    <div style="color: #94a3b8; font-size: 0.9rem;">Accident Probability</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Visual gauge
            st.markdown(f"""
                <div style="margin-top: 20px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #94a3b8; margin-bottom: 4px;">
                        <span>Low</span>
                        <span>Moderate</span>
                        <span>High</span>
                    </div>
                    <div class="risk-gauge">
                        <div class="risk-indicator" style="left: {indicator_pos}%;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Risk interpretation message
            if probability < 0.25:
                interpretation = "🟢 Conditions are favorable - standard caution advised."
                interp_color = "#22c55e"
            elif probability < 0.50:
                interpretation = "🟡 Extra caution recommended - potential adverse conditions."
                interp_color = "#eab308"
            else:
                interpretation = "🔴 High risk conditions - consider delaying travel or use extreme caution."
                interp_color = "#ef4444"
            
            st.markdown(f"""
                <div style="margin-top: 16px; padding: 12px 16px; background: rgba(30, 41, 59, 0.6); 
                border-radius: 8px; border-left: 4px solid {interp_color};">
                    <div style="font-size: 0.95rem; color: #e2e8f0;">
                        {interpretation}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with res_col2:
            # Weather Card
            weather_icon = WEATHER_ICONS.get(weather_condition, '🌡️')
            st.markdown(f"""
                <div class="weather-card">
                    <div class="weather-icon">{weather_icon}</div>
                    <div class="weather-info">
                        <div class="weather-condition">{weather_condition}</div>
                        <div class="weather-temp">{weather['temperature_f']:.0f}°F / {weather['temperature_c']:.0f}°C</div>
                        <div style="color: #94a3b8; font-size: 0.9rem;">
                            💨 Wind: {weather['windspeed']:.0f} mph
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Contributing factors
            st.markdown("""
                <div style="margin-top: 16px; padding: 12px; background: rgba(30, 41, 59, 0.5); 
                border-radius: 8px; border: 1px solid rgba(99, 102, 241, 0.2);">
                    <div style="font-size: 0.9rem; font-weight: 500; color: #e2e8f0; margin-bottom: 8px;">
                        📋 Factors Analyzed
                    </div>
                    <div style="font-size: 0.85rem; color: #94a3b8; line-height: 1.6;">
                        • Location & State<br>
                        • Current Weather Conditions<br>
                        • Time of Day<br>
                        • Vehicle Type<br>
                        • Historical Accident Patterns
                    </div>
                </div>
            """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
