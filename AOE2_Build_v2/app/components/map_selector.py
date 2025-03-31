import streamlit as st

def display_map_grid(maps, per_row=3):
    """
    Display maps as a clickable grid.
    
    Args:
        maps (list): List of map dictionaries
        per_row (int): Number of maps per row
    
    Returns:
        dict or None: Selected map or None if none selected
    """
    if not maps:
        st.warning("No maps data available.")
        return None
    
    # Search box for map
    search_term = st.text_input("Search Map", "")
    
    # Filter maps if search term is provided
    if search_term:
        filtered_maps = [m for m in maps if search_term.lower() in m["name"].lower()]
    else:
        filtered_maps = maps
    
    # Additional filters
    col1, col2 = st.columns(2)
    
    with col1:
        map_type_filter = st.multiselect(
            "Filter by Map Type",
            options=["Open", "Closed", "Hybrid", "Water"],
            default=[]
        )
    
    with col2:
        resource_filter = st.selectbox(
            "Filter by Resource Abundance",
            options=["All", "Standard", "High Resources", "Low Resources"],
            index=0
        )
    
    # Apply additional filters
    if map_type_filter:
        filtered_maps = [m for m in filtered_maps if m.get("type", "") in map_type_filter]
    
    if resource_filter != "All":
        # For a real implementation, this would filter based on resource levels
        if resource_filter == "High Resources":
            filtered_maps = [m for m in filtered_maps if any(level == "High" or level == "Abundant" for level in m.get("resources", {}).values())]
        elif resource_filter == "Low Resources":
            filtered_maps = [m for m in filtered_maps if any(level == "Low" or level == "Scarce" for level in m.get("resources", {}).values())]
    
    # Display maps count
    st.write(f"Showing {len(filtered_maps)} maps")
    
    # Create a grid of map cards
    if not filtered_maps:
        st.info("No maps match your filters.")
        return None
    
    # Create rows with the specified number of columns
    rows = [filtered_maps[i:i + per_row] for i in range(0, len(filtered_maps), per_row)]
    
    # Create a clickable card for each map
    selected_map = None
    
    for row in rows:
        cols = st.columns(per_row)
        
        for i, map_data in enumerate(row):
            with cols[i]:
                card = st.container()
                
                # Display map image if available
                if "image_path" in map_data and map_data["image_path"]:
                    card.image(map_data["image_path"], caption=map_data["name"])
                else:
                    # Placeholder for missing image
                    card.markdown(f"### {map_data['name']}")
                
                # Display map type and key characteristics
                card.caption(f"Type: {map_data.get('type', 'Unknown')}")
                
                # Display a shortened list of characteristics
                characteristics = map_data.get("characteristics", [])
                if characteristics:
                    display_chars = characteristics[:2]
                    card.write(", ".join(display_chars))
                    if len(characteristics) > 2:
                        card.caption(f"...and {len(characteristics) - 2} more")
                
                # Add a select button
                if card.button(f"Select", key=f"select_map_{map_data['id']}"):
                    selected_map = map_data
    
    return selected_map

def display_map_comparison(maps):
    """
    Display a comparison of multiple maps.
    
    Args:
        maps (list): List of map dictionaries to compare
    """
    if not maps or len(maps) < 2:
        st.warning("Please select at least two maps to compare.")
        return
    
    # Create a table for comparison
    comparison_data = []
    
    for map_data in maps:
        map_info = {
            "Map": map_data["name"],
            "Type": map_data.get("type", "Unknown"),
        }
        
        # Add resource information
        for resource, level in map_data.get("resources", {}).items():
            map_info[f"{resource.capitalize()} Level"] = level
        
        # Add key characteristics
        map_info["Key Characteristics"] = ", ".join(map_data.get("characteristics", [])[:3])
        
        comparison_data.append(map_info)
    
    # Convert to DataFrame for display
    import pandas as pd
    df = pd.DataFrame(comparison_data)
    
    st.table(df)
    
    # Additional comparison details
    st.subheader("Map Comparison Details")
    
    # Compare civilizations that perform well on each map
    for map_data in maps:
        st.write(f"### {map_data['name']} - Top Performing Civilizations")
        
        strong_civs = map_data.get("strong_civilizations_names", [])
        if strong_civs:
            for civ in strong_civs[:5]:  # Show top 5
                st.markdown(f"- {civ}")
        else:
            st.info(f"No civilization data available for {map_data['name']}")
    
    # Compare common strategies
    st.subheader("Recommended Strategies by Map")
    
    cols = st.columns(len(maps))
    for i, map_data in enumerate(maps):
        with cols[i]:
            st.write(f"**{map_data['name']}**")
            
            strategies = map_data.get("common_strategies", [])
            if strategies:
                for strategy in strategies[:3]:  # Show top 3
                    st.markdown(f"- {strategy}")
            else:
                st.info("No strategy data available") 