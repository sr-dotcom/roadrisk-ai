"""
Model loading and prediction utilities for the ABIA Traffic Accident Forecaster.

Contains functions for loading trained models and preparing prediction inputs.
"""

import joblib
import pandas as pd
from pathlib import Path
from typing import Tuple, Optional

# Note: Streamlit caching is handled in the Streamlit app, not here.
# This module provides the core loading logic.


def load_model_assets(
    model_path: Path,
    columns_path: Path
) -> Tuple[Optional[object], Optional[pd.Index]]:
    """
    Load the trained model and expected columns from pickle files.
    
    Args:
        model_path: Path to the model pickle file
        columns_path: Path to the model columns pickle file
        
    Returns:
        Tuple of (model, model_columns) or (None, None) if loading fails
    """
    try:
        model = joblib.load(model_path)
        model_columns = joblib.load(columns_path)
        return model, model_columns
    except FileNotFoundError:
        print(f"Model assets not found at {model_path} or {columns_path}")
        return None, None
    except Exception as e:
        print(f"Error loading model assets: {e}")
        return None, None


def prepare_prediction_input(
    input_df: pd.DataFrame,
    model_columns: pd.Index
) -> pd.DataFrame:
    """
    Prepare input DataFrame for model prediction.
    
    Performs one-hot encoding and aligns columns to match training format.
    
    Args:
        input_df: DataFrame with raw feature values
        model_columns: Expected column names from training
        
    Returns:
        DataFrame ready for model.predict()
    """
    # One-hot encode categorical features
    encoded_df = pd.get_dummies(input_df)
    
    # Align columns to match training format (fill missing with 0)
    final_df = encoded_df.reindex(columns=model_columns, fill_value=0)
    
    return final_df


def predict_accident_risk(
    model,
    input_df: pd.DataFrame,
    model_columns: pd.Index
) -> Tuple[int, float]:
    """
    Predict accident risk for given input.
    
    Args:
        model: Trained classifier model
        input_df: DataFrame with feature values
        model_columns: Expected column names from training
        
    Returns:
        Tuple of (prediction, probability) where:
        - prediction: 0 (low risk) or 1 (high risk)
        - probability: Probability of accident (0-1)
    """
    prepared_df = prepare_prediction_input(input_df, model_columns)
    prediction = model.predict(prepared_df)[0]
    probability = model.predict_proba(prepared_df)[0][1]
    
    return prediction, probability
