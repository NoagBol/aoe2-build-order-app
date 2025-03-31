# Import from the file with emoji
import importlib.util
import sys
import os
import streamlit as st

# Get the full path to the module file
file_path = os.path.join(os.path.dirname(__file__), '3_🗺️_Map_Analysis.py')

# Create a module spec
spec = importlib.util.spec_from_file_location('map_analysis_module', file_path)

# Create a module from the spec
module = importlib.util.module_from_spec(spec)

# Add the module to sys.modules
sys.modules['map_analysis_module'] = module

# Execute the module
spec.loader.exec_module(module)

# Define a function to call the main function of the module
def show_map_analysis_page():
    """Show the map analysis page."""
    # Monkey patch set_page_config to prevent it from being called again
    original_set_page_config = st.set_page_config
    st.set_page_config = lambda **kwargs: None
    
    # Call the module's main function
    module.main()
    
    # Restore original set_page_config
    st.set_page_config = original_set_page_config 