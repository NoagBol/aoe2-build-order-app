import streamlit as st
import os
from pathlib import Path

# Import application modules
from app.utils.utils import apply_streamlit_theme
from app.utils.session_state_manager import initialize_session_state, check_navigation
from app.utils.data_loader import load_civilizations, load_featured_build_orders, load_maps
from app.initialize import initialize_app

# Import page modules
from app.pages.home import show_home_page
from app.pages.build_orders import show_build_orders
from app.pages.map_analysis import show_map_analysis_page
from app.pages.matchup_analysis import show_matchup_analysis_page
from app.pages.statistics import show_statistics_page
from app.pages.about import show_about_page
from app.pages.profile import show_profile_page

# Configure the page - must be the first Streamlit command
st.set_page_config(
    page_title="AOE2 Build Order Advisor",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Setup app if needed
app_root = Path(__file__).parent / 'app'
assets_dir = app_root / 'assets'
if not assets_dir.exists():
    initialize_app()

# Apply streamlit theme
apply_streamlit_theme()

# Initialize session state
initialize_session_state()

# Create a horizontal menu at the top
menu_items = {
    "Home": show_home_page,
    "Build Orders": show_build_orders,
    "Map Analysis": show_map_analysis_page,
    "Matchup Analysis": show_matchup_analysis_page,
    "Statistics": show_statistics_page,
    "About": show_about_page,
    "Profile": show_profile_page
}

# Create columns for the menu with extra space for Profile
cols = st.columns([1, 1, 1, 1, 1, 1, 2])

# Add menu buttons
for i, (name, func) in enumerate(menu_items.items()):
    with cols[i]:
        if st.button(name, key=f"menu_{name}"):
            st.session_state.current_page = name
            st.rerun()

# Display the current page
current_page = st.session_state.get("current_page", "Home")
menu_items[current_page]()

# Display sidebar content
st.sidebar.markdown("---")

# Featured build orders
st.sidebar.header("Featured Build Orders")
featured_builds = load_featured_build_orders()

for build in featured_builds[:3]:  # Display up to 3 featured builds
    st.sidebar.markdown(f"**{build['name']}**")
    st.sidebar.markdown(f"*{build['type']} - {build['difficulty']}*")
    if st.sidebar.button(f"View {build['name']}", key=f"sidebar_build_{build['id']}"):
        st.session_state.selected_build_order = build
        st.session_state.current_page = "Build Orders"
        st.rerun()

# Add quick civilization selector
st.sidebar.markdown("---")
st.sidebar.header("Quick Civilization Lookup")

civilizations = load_civilizations()
civ_names = [civ["name"] for civ in civilizations]
selected_civ_name = st.sidebar.selectbox("Select civilization", civ_names)

if selected_civ_name:
    selected_civ = next((civ for civ in civilizations if civ["name"] == selected_civ_name), None)
    if selected_civ:
        st.sidebar.markdown(f"**{selected_civ['name']}**")
        st.sidebar.markdown(f"*{selected_civ['specialty']}*")
        st.sidebar.markdown("**Unique Units:**")
        for unit in selected_civ["unique_units"]:
            st.sidebar.markdown(f"- {unit}")
        st.sidebar.markdown("**Unique Techs:**")
        for tech in selected_civ["unique_techs"]:
            st.sidebar.markdown(f"- {tech}")
        st.sidebar.markdown("**Civilization Bonuses:**")
        for bonus in selected_civ["civilization_bonuses"]:
            st.sidebar.write(f"- {bonus}")

# Footer
st.sidebar.markdown("---")
st.sidebar.info(
    "Made with ❤️ for Age of Empires II: DE players. "
    "This app helps you learn and master build orders."
)
st.sidebar.markdown("© 2023 AoE2 Build Order Advisor") 