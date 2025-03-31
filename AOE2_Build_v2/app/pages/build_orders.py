import streamlit as st
from app.components.build_order_display import display_build_order_list, display_build_order_detail
from app.components.build_order_submission import (
    display_build_order_submission_form,
    display_user_submissions
)
from app.utils.data_loader import load_build_orders, load_civilizations

def show_build_orders():
    """Display the build orders page."""
    st.title("Build Orders")
    
    # Create tabs for different sections
    tabs = st.tabs([
        "Community Build Orders",
        "Submit Build Order",
        "Your Submissions"
    ])
    
    # Load civilizations into session state if not already loaded
    if "civilizations" not in st.session_state:
        st.session_state.civilizations = load_civilizations()
    
    with tabs[0]:
        # Load and display community build orders
        build_orders = load_build_orders()
        selected_bo = display_build_order_list(build_orders)
        
        if selected_bo:
            st.session_state.selected_build_order = selected_bo
            display_build_order_detail(selected_bo)
    
    with tabs[1]:
        # Display build order submission form
        display_build_order_submission_form()
    
    with tabs[2]:
        # Display user's submitted build orders
        display_user_submissions() 