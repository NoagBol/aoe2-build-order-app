import streamlit as st
import sys
import os
import pandas as pd

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.map_selector import display_map_grid
from utils.data_loader import load_maps, load_map_specific_strategies
from utils.recommendation_engine import get_map_civilization_tier_list, get_recommended_build_orders
from components.build_order_display import display_build_order_list

def display_tier_list(tier_list):
    """Display civilization tier list for a map."""
    if not tier_list:
        st.info("No tier data available for this map.")
        return
    
    # Create tabs for each tier
    tier_tabs = st.tabs(["S Tier", "A Tier", "B Tier", "C Tier", "D Tier"])
    
    for i, tab in enumerate(tier_tabs):
        with tab:
            tier_letter = ["S", "A", "B", "C", "D"][i]
            tier_civs = [civ for civ in tier_list if civ["tier"] == tier_letter]
            
            if not tier_civs:
                st.write(f"No civilizations in {tier_letter} Tier")
                continue
            
            # Display as a grid
            cols = st.columns(3)
            for j, civ in enumerate(tier_civs):
                with cols[j % 3]:
                    st.subheader(civ["name"])
                    st.caption(f"Win Rate: {civ['win_rate']}%")
                    st.write(civ["strengths_on_map"])

def display_map_strategies(strategies):
    """Display map-specific strategies."""
    if not strategies:
        st.info("No specific strategies available for this map.")
        return
    
    for strategy in strategies:
        with st.expander(f"{strategy['name']} ({strategy['type']})"):
            st.write(strategy["description"])
            st.subheader("Key Points")
            for point in strategy["key_points"]:
                st.markdown(f"- {point}")
            
            st.subheader("Suitable Civilizations")
            st.write(", ".join(strategy["suitable_civilizations"]))

def main():
    st.set_page_config(
        page_title="Map Analysis & Strategies",
        page_icon="🗺️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("Map Analysis & Strategies")
    
    # Map selection
    maps = load_maps()
    selected_map = display_map_grid(maps)
    
    if selected_map:
        st.session_state.selected_map = selected_map
        
        # Display map details
        st.header(f"{selected_map['name']} - {selected_map['type']} Map")
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            # Display map image if available
            if "image_path" in selected_map and selected_map["image_path"]:
                st.image(selected_map["image_path"], caption=selected_map["name"])
            else:
                st.info("Map preview not available")
            
            # Map characteristics
            st.subheader("Map Characteristics")
            for char in selected_map.get("characteristics", []):
                st.markdown(f"- {char}")
        
        with col2:
            # Resources information
            st.subheader("Resources")
            resources = selected_map.get("resources", {})
            if resources:
                resources_df = pd.DataFrame({
                    "Resource": list(resources.keys()),
                    "Availability": list(resources.values())
                })
                st.table(resources_df)
            
            # Starting resources
            st.subheader("Starting Resources")
            starting_resources = selected_map.get("starting_resources", {})
            if starting_resources:
                start_resources_df = pd.DataFrame({
                    "Resource": list(starting_resources.keys()),
                    "Amount": list(starting_resources.values())
                })
                st.table(start_resources_df)
        
        # Civilization tier list for this map
        st.header("Civilization Performance on This Map")
        tier_list = get_map_civilization_tier_list(selected_map["id"])
        display_tier_list(tier_list)
        
        # Map-specific strategies
        st.header("Recommended Strategies")
        map_strategies = load_map_specific_strategies(selected_map["id"])
        display_map_strategies(map_strategies)
        
        # Selected civilization analysis (if one is selected)
        if "selected_civilization" in st.session_state:
            civ = st.session_state.selected_civilization
            st.header(f"{civ['name']} on {selected_map['name']}")
            
            # Get map-specific build orders for the civilization
            civ_map_builds = get_recommended_build_orders(
                civilization_id=civ["id"],
                map_type=selected_map["name"]
            )
            
            if civ_map_builds:
                st.subheader("Recommended Build Orders")
                display_build_order_list(civ_map_builds, compact=True)
            else:
                st.info(f"No specific build orders found for {civ['name']} on {selected_map['name']}.")

if __name__ == "__main__":
    main() 