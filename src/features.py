"""
Feature engineering functions for the ABIA Traffic Accident Forecaster.

Contains functions for creating time-based and weather-based features.
"""

import pandas as pd
from .config import WEATHER_CODE_MAP


def get_part_of_day(hour: int) -> str:
    """
    Categorize hour into part of day.
    
    Args:
        hour: Hour of day (0-23)
        
    Returns:
        'Morning' (5-11), 'Afternoon' (12-16), 'Evening' (17-20), or 'Night' (21-4)
    """
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 21:
        return 'Evening'
    else:
        return 'Night'


def map_weather_condition(weathercode: int) -> str:
    """
    Map WMO weather code to human-readable condition.
    
    Args:
        weathercode: WMO weather interpretation code from Open-Meteo API
        
    Returns:
        Human-readable weather condition string
    """
    return WEATHER_CODE_MAP.get(weathercode, 'Other')


def create_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create time-based features from DateTime column.
    
    Features created:
    - Hour: Hour of day (0-23)
    - DayOfWeek: Day name (e.g., 'Monday')
    - Month: Month number (1-12)
    - PartOfDay: 'Morning', 'Afternoon', 'Evening', or 'Night'
    
    Args:
        df: DataFrame with 'DateTime' column
        
    Returns:
        DataFrame with new time features added
    """
    df = df.copy()
    
    # Ensure DateTime is in correct format
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    
    # Create features
    df['Hour'] = df['DateTime'].dt.hour
    df['DayOfWeek'] = df['DateTime'].dt.day_name()
    df['Month'] = df['DateTime'].dt.month
    df['PartOfDay'] = df['Hour'].apply(get_part_of_day)
    
    return df


def create_weather_condition(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create human-readable weather condition from weather code.
    
    Args:
        df: DataFrame with 'weathercode' column
        
    Returns:
        DataFrame with 'WeatherCondition' column added
    """
    df = df.copy()
    df['WeatherCondition'] = df['weathercode'].map(WEATHER_CODE_MAP).fillna('Other')
    return df


def create_model_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create all features needed for the prediction model.
    
    Combines time features and weather condition mapping.
    
    Args:
        df: DataFrame with DateTime and weathercode columns
        
    Returns:
        DataFrame with all model features added
    """
    df = create_time_features(df)
    df = create_weather_condition(df)
    return df
