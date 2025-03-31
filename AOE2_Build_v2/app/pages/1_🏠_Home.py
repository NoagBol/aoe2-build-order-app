import streamlit as st
import sys
import os

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.civilization_selector import display_civilization_grid
from utils.data_loader import load_civilizations, load_featured_build_orders
from utils.session_state_manager import initialize_session_state

def display_featured_build_orders(featured_builds):
    """Display featured build orders in a grid layout."""
    if not featured_builds:
        st.info("No featured build orders available.")
        return
    
    # Display in a 2-column grid
    cols = st.columns(2)
    for i, build in enumerate(featured_builds):
        with cols[i % 2]:
            st.subheader(build["name"])
            st.caption(f"Type: {build['type']} | Difficulty: {build['difficulty']}")
            st.write(build["description"])
            if st.button(f"View Details", key=f"view_build_{build['id']}"):
                st.session_state.selected_build_order = build
                st.session_state.page_to_navigate = "Build_Orders"
                st.experimental_rerun()

def display_meta_updates():
    """Display recent meta updates."""
    meta_updates = [
        {
            "version": "Update 101.102.3476.0",
            "date": "2023-11-01",
            "changes": [
                "Gurjaras: Reduced Shrivamsha Rider anti-ranged armor by 1",
                "Hindustanis: Imperial Camel Rider hit points reduced from 160 to 150",
                "Bengalis: Fixed Rathas not benefiting from Bloodlines tech",
                "Poles: Stone mining gold generation reduced by 15%"
            ]
        }
    ]
    
    for update in meta_updates:
        st.markdown(f"**{update['version']}** ({update['date']})")
        for change in update["changes"]:
            st.markdown(f"- {change}")

def main():
    st.set_page_config(
        page_title="AoE2:DE Build Order Advisor",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state if first visit
    initialize_session_state()
    
    # Page layout
    st.title("Age of Empires II: Build Order Advisor")
    st.markdown("""
    Welcome to your expert build order advisor for Age of Empires II: Definitive Edition!
    Select your civilization to get started with tailored build order recommendations.
    """)
    
    # Quick start panel
    st.header("Select Your Civilization")
    
    # We'll simulate the civilization data for now
    # In a complete implementation, this would come from a database
    civilizations = load_civilizations()
    
    selected_civ = display_civilization_grid(civilizations)
    
    if selected_civ:
        st.session_state.selected_civilization = selected_civ
        st.success(f"Selected: {selected_civ['name']}")
        
        # Quick action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("View Recommended Builds"):
                st.session_state.page_to_navigate = "Build_Orders"
                st.experimental_rerun()
        with col2:
            if st.button("Analyze Matchups"):
                st.session_state.page_to_navigate = "Matchup_Analysis"
                st.experimental_rerun()
        with col3:
            if st.button("Map-specific Strategies"):
                st.session_state.page_to_navigate = "Map_Analysis"
                st.experimental_rerun()
    
    # Featured build orders
    st.header("Featured Build Orders")
    featured_builds = load_featured_build_orders()
    display_featured_build_orders(featured_builds)
    
    # Recent meta updates
    st.header("Recent Meta Updates")
    display_meta_updates()

if __name__ == "__main__":
    main() 