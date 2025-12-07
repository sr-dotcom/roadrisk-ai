"""
Configuration constants and mappings for the ABIA Traffic Accident Forecaster.
"""

# --- Supported States ---
STATE_LIST = ['DC', 'PA', 'FL', 'NC', 'NY', 'CA']

# --- Vehicle Type Mappings ---
VEHICLE_MAP = {
    'Automobile': '02 - Automobile',
    'Light Duty Truck': '05 - Light Duty Truck',
    'Station Wagon': '03 - Station Wagon',
    'Heavy Duty Truck': '06 - Heavy Duty Truck',
    'Other': '28 - Other',
    'Unknown': '29 - Unknown'
}

# --- Gender Mappings ---
GENDER_MAP = {
    'Male': 'M',
    'Female': 'F',
    'Unknown': 'U'
}

# --- WMO Weather Interpretation Codes ---
# Maps numeric weather codes from Open-Meteo API to human-readable descriptions
WEATHER_CODE_MAP = {
    0: 'Clear',
    1: 'Mainly Clear',
    2: 'Partly Cloudy',
    3: 'Overcast',
    45: 'Fog',
    48: 'Depositing Rime Fog',
    51: 'Light Drizzle',
    53: 'Moderate Drizzle',
    55: 'Dense Drizzle',
    56: 'Light Freezing Drizzle',
    57: 'Dense Freezing Drizzle',
    61: 'Slight Rain',
    63: 'Moderate Rain',
    65: 'Heavy Rain',
    66: 'Light Freezing Rain',
    67: 'Heavy Freezing Rain',
    71: 'Slight Snowfall',
    73: 'Moderate Snowfall',
    75: 'Heavy Snowfall',
    77: 'Snow Grains',
    80: 'Slight Rain Showers',
    81: 'Moderate Rain Showers',
    82: 'Violent Rain Showers',
    85: 'Slight Snow Showers',
    86: 'Heavy Snow Showers',
    95: 'Thunderstorm',
    96: 'Thunderstorm with Slight Hail',
    99: 'Thunderstorm with Heavy Hail'
}

# --- Columns to Drop During Data Cleaning ---
COLUMNS_TO_DROP = [
    'SeqID', 'Date Of Stop', 'Time Of Stop', 'Agency', 'SubAgency',
    'Belts', 'Personal Injury', 'Property Damage', 'Fatal', 'Commercial License',
    'HAZMAT', 'Commercial Vehicle', 'Alcohol', 'Work Zone', 'Search Conducted',
    'Search Disposition', 'Search Outcome', 'Search Reason', 'Search Reason For Stop',
    'Search Type', 'Search Arrest Reason', 'Violation Type', 'Charge',
    'Article', 'Driver City', 'Driver State', 'DL State', 'Arrest Type', 'Geolocation'
]

# --- Model Features ---
MODEL_FEATURES = [
    'temperature', 'precipitation', 'snowfall', 'windspeed',
    'Hour', 'DayOfWeek', 'Month', 'PartOfDay', 'WeatherCondition',
    'VehicleType', 'State', 'Gender'
]

CATEGORICAL_FEATURES = [
    'DayOfWeek', 'Month', 'PartOfDay', 'WeatherCondition',
    'VehicleType', 'State', 'Gender'
]
