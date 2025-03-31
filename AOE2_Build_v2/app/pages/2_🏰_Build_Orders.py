import streamlit as st
import sys
import os
import pandas as pd

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.build_order_display import display_build_order_list, display_build_order_detail
from utils.data_loader import load_build_orders, load_civilizations
from utils.recommendation_engine import get_recommended_build_orders
from utils.session_state_manager import check_navigation, get_selected_civilization

def main():
    st.set_page_config(
        page_title="Build Order Recommendations",
        page_icon="🏰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Check if navigating from another page
    check_navigation()
    
    st.title("Build Order Recommendations")
    
    # Get selected civilization or prompt to select
    selected_civ = get_selected_civilization()
    if not selected_civ:
        st.warning("Please select a civilization first")
        if st.button("Go to Civilization Selection"):
            st.session_state.page_to_navigate = "Home"
            st.experimental_rerun()
        return
    
    st.subheader(f"Recommended Build Orders for {selected_civ['name']}")
    
    # Sidebar filters
    with st.sidebar:
        st.header("Filters")
        
        # Build order type filter
        build_types = ["All", "Fast Castle", "Feudal Rush", "Scout Rush", 
                      "Archer Rush", "Men-at-Arms Rush", "Tower Rush", 
                      "Fast Imperial", "Boom", "Water Strategy"]
        selected_type = st.multiselect("Build Order Type", build_types, default=["All"])
        
        # Map type filter
        map_types = ["All", "Arabia", "Arena", "Islands", "Black Forest", "Nomad", 
                    "Gold Rush", "Highland", "Mediterranean"]
        selected_map = st.selectbox("Map Type", map_types, index=0)
        
        # Difficulty filter
        difficulties = ["All", "Beginner", "Intermediate", "Advanced", "Expert"]
        selected_difficulty = st.selectbox("Difficulty Level", difficulties, index=0)
        
        # Team composition
        st.subheader("Team Composition (Optional)")
        civilizations = load_civilizations()
        ally_civs = st.multiselect("Allied Civilizations", 
                                  [civ["name"] for civ in civilizations if civ["name"] != selected_civ["name"]])
        
        # Enemy composition
        st.subheader("Enemy Composition (Optional)")
        enemy_civs = st.multiselect("Enemy Civilizations", 
                                   [civ["name"] for civ in civilizations])
        
        # Apply filters button
        apply_filters = st.button("Apply Filters")
    
    # Get recommended build orders based on filters
    if apply_filters or "recommended_builds" not in st.session_state:
        with st.spinner("Finding optimal build orders..."):
            recommended_builds = get_recommended_build_orders(
                civilization_id=selected_civ["id"],
                build_types=[] if "All" in selected_type else selected_type,
                map_type=None if selected_map == "All" else selected_map,
                difficulty=None if selected_difficulty == "All" else selected_difficulty,
                ally_civs=ally_civs,
                enemy_civs=enemy_civs
            )
            st.session_state.recommended_builds = recommended_builds
    
    # Display build orders
    if hasattr(st.session_state, 'recommended_builds') and st.session_state.recommended_builds:
        # Display as cards with expandable details
        selected_build = display_build_order_list(st.session_state.recommended_builds)
        
        if selected_build:
            st.session_state.selected_build_order = selected_build
            display_build_order_detail(selected_build)
    else:
        st.info("No build orders match your criteria. Try adjusting your filters.")

if __name__ == "__main__":
    main() 