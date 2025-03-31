import streamlit as st

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if "selected_civilization" not in st.session_state:
        st.session_state.selected_civilization = None
    
    if "selected_map" not in st.session_state:
        st.session_state.selected_map = None
    
    if "selected_build_order" not in st.session_state:
        st.session_state.selected_build_order = None
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"
    
    if "recommended_builds" not in st.session_state:
        st.session_state.recommended_builds = []

def check_navigation():
    """Check if we need to navigate to a different page and reset navigation state."""
    # This function would handle navigation logic between different pages
    # in a real Streamlit multipage app, but we're simulating this behavior
    if "page_to_navigate" in st.session_state and st.session_state.page_to_navigate:
        # In a real app, we would navigate to the specified page
        # Here we just reset the navigation state since we're already on the page
        page = st.session_state.page_to_navigate
        st.session_state.page_to_navigate = None
        return page
    return None

def get_selected_civilization():
    """Get the currently selected civilization from session state."""
    if "selected_civilization" in st.session_state and st.session_state.selected_civilization:
        return st.session_state.selected_civilization
    return None

def get_selected_map():
    """Get the currently selected map from session state."""
    if "selected_map" in st.session_state and st.session_state.selected_map:
        return st.session_state.selected_map
    return None

def get_selected_build_order():
    """Get the currently selected build order from session state."""
    if "selected_build_order" in st.session_state and st.session_state.selected_build_order:
        return st.session_state.selected_build_order
    return None

def save_to_favorites(build_order_id, user_id=None, notes=None):
    """Save a build order to the user's favorites."""
    # In a real app, this would interact with a database
    # Here we just update session state
    if "favorites" not in st.session_state:
        st.session_state.favorites = []
    
    # Check if already in favorites
    if build_order_id not in [fav.get("build_order_id") for fav in st.session_state.favorites]:
        st.session_state.favorites.append({
            "build_order_id": build_order_id,
            "user_id": user_id or "default_user",
            "notes": notes,
            "date_added": "Today"  # In a real app, this would be a proper timestamp
        })
        return True
    return False

def remove_from_favorites(build_order_id, user_id=None):
    """Remove a build order from the user's favorites."""
    # In a real app, this would interact with a database
    # Here we just update session state
    if "favorites" in st.session_state:
        st.session_state.favorites = [
            fav for fav in st.session_state.favorites 
            if fav.get("build_order_id") != build_order_id or 
               (user_id and fav.get("user_id") != user_id)
        ]
        return True
    return False

def get_favorites(user_id=None):
    """Get the user's favorite build orders."""
    # In a real app, this would retrieve from a database
    # Here we just return from session state
    if "favorites" in st.session_state:
        if user_id:
            return [fav for fav in st.session_state.favorites if fav.get("user_id") == user_id]
        return st.session_state.favorites
    return [] 