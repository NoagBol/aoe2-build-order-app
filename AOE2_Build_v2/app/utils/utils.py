import os
import json
import streamlit as st
from pathlib import Path

def get_app_root():
    """Get the root directory of the application."""
    current_file = Path(__file__)
    # Go up two levels: from /app/utils/utils.py to /app
    return current_file.parent.parent

def get_asset_path(asset_type, asset_name):
    """
    Get the path to an asset file.
    
    Args:
        asset_type (str): Type of asset (images, icons, data)
        asset_name (str): Name of the asset file
    
    Returns:
        str: Path to the asset
    """
    app_root = get_app_root()
    return os.path.join(app_root, 'assets', asset_type, asset_name)

def load_json_asset(asset_name):
    """
    Load a JSON asset file.
    
    Args:
        asset_name (str): Name of the JSON file in the data directory
    
    Returns:
        dict: Loaded JSON data or empty dict if file not found
    """
    json_path = get_asset_path('data', asset_name)
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_json_asset(data, asset_name):
    """
    Save data to a JSON asset file.
    
    Args:
        data (dict): Data to save
        asset_name (str): Name of the JSON file in the data directory
    
    Returns:
        bool: True if successful, False otherwise
    """
    json_path = get_asset_path('data', asset_name)
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    try:
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
        return True
    except Exception:
        return False

def format_time(seconds):
    """
    Format time in seconds to a human-readable string.
    
    Args:
        seconds (int): Time in seconds
    
    Returns:
        str: Formatted time string (e.g., "12:34")
    """
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02d}"

def format_age(age):
    """
    Format age to a human-readable string.
    
    Args:
        age (str): Age code (e.g., "dark", "feudal", "castle", "imperial")
    
    Returns:
        str: Formatted age string (e.g., "Dark Age")
    """
    age_map = {
        "dark": "Dark Age",
        "feudal": "Feudal Age",
        "castle": "Castle Age",
        "imperial": "Imperial Age"
    }
    return age_map.get(age.lower(), age)

def get_difficulty_color(difficulty):
    """
    Get a color for a difficulty level.
    
    Args:
        difficulty (str): Difficulty level (e.g., "Easy", "Medium", "Hard")
    
    Returns:
        str: Color code
    """
    difficulty_colors = {
        "Beginner": "#4CAF50",  # Green
        "Easy": "#8BC34A",      # Light Green
        "Medium": "#FFC107",    # Amber
        "Hard": "#FF9800",      # Orange
        "Expert": "#F44336"     # Red
    }
    return difficulty_colors.get(difficulty, "#9E9E9E")  # Default gray

def get_build_type_icon(build_type):
    """
    Get an icon name for a build type.
    
    Args:
        build_type (str): Build type (e.g., "Fast Castle", "Rush", "Boom")
    
    Returns:
        str: Icon name from streamlit-icons
    """
    build_type_icons = {
        "Fast Castle": "rocket",
        "Rush": "lightning",
        "Boom": "graph-up",
        "Water": "water",
        "Defensive": "shield",
        "Aggressive": "sword",
        "Hybrid": "shuffle",
    }
    return build_type_icons.get(build_type, "info-circle")

def apply_streamlit_theme():
    """Apply custom theme to Streamlit app."""
    # Custom CSS
    st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        margin-top: 10px;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        background-color: white;
    }
    .stSelectbox>div>div>select {
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True) 