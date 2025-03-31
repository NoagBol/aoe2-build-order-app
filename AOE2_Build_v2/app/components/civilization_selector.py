import streamlit as st

def display_civilization_grid(civilizations, per_row=6):
    """
    Display civilizations as a clickable grid.
    
    Args:
        civilizations (list): List of civilization dictionaries
        per_row (int): Number of civilizations per row
    
    Returns:
        dict or None: Selected civilization or None if none selected
    """
    if not civilizations:
        st.warning("No civilizations data available.")
        return None
    
    # Search box for civilization
    search_term = st.text_input("Search Civilization", "")
    
    # Filter civilizations if search term is provided
    if search_term:
        filtered_civs = [civ for civ in civilizations if search_term.lower() in civ["name"].lower()]
    else:
        filtered_civs = civilizations
    
    # Specialty filter
    specialty_filter = st.multiselect(
        "Filter by Specialty",
        options=["Archers", "Cavalry", "Infantry", "Siege", "Naval", "Monks", "Economy", "Gunpowder"],
        default=[]
    )
    
    # Apply specialty filter
    if specialty_filter:
        filtered_civs = [civ for civ in filtered_civs if any(spec in specialty_filter for spec in civ.get("specialty", []))]
    
    # Display civs count
    st.write(f"Showing {len(filtered_civs)} civilizations")
    
    # Create a grid of civilization cards
    if not filtered_civs:
        st.info("No civilizations match your filters.")
        return None
    
    # Create rows with the specified number of columns
    rows = [filtered_civs[i:i + per_row] for i in range(0, len(filtered_civs), per_row)]
    
    # Create a clickable card for each civilization
    selected_civ = None
    
    for row in rows:
        cols = st.columns(per_row)
        
        for i, civ in enumerate(row):
            with cols[i]:
                card = st.container()
                
                # Display civilization icon if available
                if "icon_path" in civ and civ["icon_path"]:
                    card.image(civ["icon_path"], width=80)
                else:
                    # Placeholder for missing icon
                    card.markdown("🏰")
                
                card.subheader(civ["name"])
                card.caption(f"Specialty: {', '.join(civ.get('specialty', ['None']))}")
                
                # Add a select button
                if card.button(f"Select", key=f"select_{civ['id']}"):
                    selected_civ = civ
    
    return selected_civ

def display_civilization_multiselect(civilizations, max_selections=None, key=None):
    """
    Display civilizations as a multi-select grid.
    
    Args:
        civilizations (list): List of civilization dictionaries
        max_selections (int): Maximum number of selections allowed (None for unlimited)
        key (str): Unique key for the component
    
    Returns:
        list: List of selected civilizations
    """
    if not civilizations:
        st.warning("No civilizations data available.")
        return []
    
    # Initialize session state for selections if not already present
    if f"selected_civs_{key}" not in st.session_state:
        st.session_state[f"selected_civs_{key}"] = []
    
    # Search box for civilization
    search_term = st.text_input(f"Search Civilization", "", key=f"search_{key}")
    
    # Filter civilizations if search term is provided
    if search_term:
        filtered_civs = [civ for civ in civilizations if search_term.lower() in civ["name"].lower()]
    else:
        filtered_civs = civilizations
    
    # Display the current selections
    st.write("Selected: " + ", ".join([civ["name"] for civ in st.session_state[f"selected_civs_{key}"]]))
    
    if max_selections and len(st.session_state[f"selected_civs_{key}"]) >= max_selections:
        st.warning(f"Maximum of {max_selections} selections allowed. Deselect one to select another.")
    
    # Create selection grid
    cols = st.columns(4)
    
    for i, civ in enumerate(filtered_civs):
        with cols[i % 4]:
            # Check if already selected
            is_selected = any(selected_civ["id"] == civ["id"] for selected_civ in st.session_state[f"selected_civs_{key}"])
            
            if is_selected:
                if st.button(f"✓ {civ['name']}", key=f"civ_{civ['id']}_{key}"):
                    # Remove from selections
                    st.session_state[f"selected_civs_{key}"] = [
                        selected_civ for selected_civ in st.session_state[f"selected_civs_{key}"] 
                        if selected_civ["id"] != civ["id"]
                    ]
                    st.experimental_rerun()
            else:
                # Only allow selection if under max_selections
                if not max_selections or len(st.session_state[f"selected_civs_{key}"]) < max_selections:
                    if st.button(civ['name'], key=f"civ_{civ['id']}_{key}"):
                        st.session_state[f"selected_civs_{key}"].append(civ)
                        st.experimental_rerun()
    
    # Clear selections button
    if st.session_state[f"selected_civs_{key}"] and st.button("Clear Selections", key=f"clear_{key}"):
        st.session_state[f"selected_civs_{key}"] = []
        st.experimental_rerun()
    
    return st.session_state[f"selected_civs_{key}"] 