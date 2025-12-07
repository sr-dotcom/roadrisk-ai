"""
Data processing functions for the ABIA Traffic Accident Forecaster.

Contains functions for cleaning, filtering, and preparing traffic violation data.
"""

import pandas as pd
from .config import COLUMNS_TO_DROP, STATE_LIST


def clean_traffic_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw traffic violation data.
    
    Operations:
    - Combine Date and Time into DateTime column
    - Remove rows with invalid (0.0) or missing coordinates
    - Convert 'Accident' column to binary (1 for Yes, 0 for No)
    - Drop unnecessary columns
    
    Args:
        df: Raw traffic violations DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    df = df.copy()
    
    # Combine Date and Time into DateTime
    df['DateTime'] = pd.to_datetime(df['Date Of Stop'] + ' ' + df['Time Of Stop'])
    
    # Remove invalid coordinates
    df = df[df['Latitude'] != 0.0]
    df = df[df['Longitude'] != 0.0]
    df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    
    # Convert Accident to binary
    df['Accident'] = df['Accident'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    # Drop unnecessary columns
    cols_to_drop = [c for c in COLUMNS_TO_DROP if c in df.columns]
    df.drop(columns=cols_to_drop, inplace=True)
    
    return df


def filter_by_states(df: pd.DataFrame, states: list = None) -> pd.DataFrame:
    """
    Filter DataFrame to include only specified states.
    
    Args:
        df: DataFrame with 'State' column
        states: List of state codes to include (defaults to STATE_LIST from config)
        
    Returns:
        Filtered DataFrame
    """
    if states is None:
        states = STATE_LIST
    
    return df[df['State'].isin(states)].copy()


def prepare_weather_lookup_keys(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare DataFrame for weather API lookup by creating rounded coordinates and date.
    
    Args:
        df: DataFrame with Latitude, Longitude, and DateTime columns
        
    Returns:
        DataFrame with lat_round, lon_round, and date_only columns added
    """
    df = df.copy()
    df['lat_round'] = df['Latitude'].round(4)
    df['lon_round'] = df['Longitude'].round(4)
    df['date_only'] = df['DateTime'].dt.date
    return df


def remove_missing_weather(df: pd.DataFrame, weather_column: str = 'temperature') -> pd.DataFrame:
    """
    Remove rows with missing weather data.
    
    Args:
        df: DataFrame with weather columns
        weather_column: Column to check for missing values (if null, all weather data is missing)
        
    Returns:
        DataFrame with missing weather rows removed
    """
    return df.dropna(subset=[weather_column]).copy()
