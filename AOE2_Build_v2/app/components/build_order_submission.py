import streamlit as st
from datetime import datetime
from app.utils.database import save_build_order, get_user_build_orders
from app.utils.data_loader import load_maps

def display_build_order_submission_form():
    """Display the build order submission form."""
    if "user_id" not in st.session_state:
        st.warning("Please log in to submit build orders.")
        return
    
    st.subheader("Submit Your Build Order")
    
    # Load maps data if not in session state
    if "maps" not in st.session_state:
        st.session_state.maps = load_maps()
    
    with st.form("build_order_submission"):
        # Basic Information
        st.markdown("### Basic Information")
        name = st.text_input("Build Order Name")
        description = st.text_area("Description")
        build_type = st.selectbox("Build Type", [
            "Fast Castle",
            "Scout Rush",
            "Archer Rush",
            "Man-at-Arms Rush",
            "Drush",
            "Tower Rush",
            "Boom",
            "Water",
            "Hybrid",
            "Other"
        ])
        difficulty = st.select_slider("Difficulty", options=["Beginner", "Intermediate", "Advanced"])
        primary_goal = st.text_input("Primary Goal")
        execution_time = st.text_input("Execution Time (e.g., '12-14 minutes')")
        
        # Resource Allocation
        st.markdown("### Resource Allocation")
        col1, col2 = st.columns(2)
        with col1:
            food_vills = st.number_input("Food Villagers", min_value=0, max_value=100, value=0)
            wood_vills = st.number_input("Wood Villagers", min_value=0, max_value=100, value=0)
        with col2:
            gold_vills = st.number_input("Gold Villagers", min_value=0, max_value=100, value=0)
            stone_vills = st.number_input("Stone Villagers", min_value=0, max_value=100, value=0)
        
        # Build Order Steps
        st.markdown("### Build Order Steps")
        st.info("Enter each step of your build order. You can add up to 20 steps.")
        
        # Initialize steps in session state if not present
        if "build_order_steps" not in st.session_state:
            st.session_state.build_order_steps = []
        
        # Display existing steps
        for i, step in enumerate(st.session_state.build_order_steps):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(f"Step {i+1}: {step}")
            with col2:
                if st.button("Remove", key=f"remove_step_{i}"):
                    st.session_state.build_order_steps.pop(i)
                    st.rerun()
        
        # Add new step
        if len(st.session_state.build_order_steps) < 20:
            new_step = st.text_input("Add New Step")
            if st.button("Add Step") and new_step:
                st.session_state.build_order_steps.append(new_step)
                st.rerun()
        
        # Additional Details
        st.markdown("### Additional Details")
        # Get civilization list safely
        civ_names = []
        if "civilizations" in st.session_state:
            civ_names = [civ.get("name", "") for civ in st.session_state.civilizations if civ.get("name")]
        
        ideal_civs = st.multiselect("Ideal Civilizations", ["All"] + civ_names)
        suitable_maps = st.multiselect("Suitable Maps", ["All"] + [map["name"] for map in st.session_state.maps])
        tips = st.text_area("Tips and Tricks")
        
        # Video Tutorial
        st.markdown("### Video Tutorial (Optional)")
        video_url = st.text_input("Video Tutorial URL")
        
        # Additional Notes
        st.markdown("### Additional Notes (Optional)")
        notes = st.text_area("Additional Notes")
        
        # Submit Button
        if st.form_submit_button("Submit Build Order"):
            if not name:
                st.error("Please provide a name for your build order.")
                return
            
            if not st.session_state.build_order_steps:
                st.error("Please add at least one step to your build order.")
                return
            
            build_order = {
                "name": name,
                "description": description,
                "type": build_type,
                "difficulty": difficulty,
                "primary_goal": primary_goal,
                "execution_time": execution_time,
                "resource_allocation": {
                    "food": food_vills,
                    "wood": wood_vills,
                    "gold": gold_vills,
                    "stone": stone_vills
                },
                "steps": st.session_state.build_order_steps,
                "ideal_civilizations": ideal_civs,
                "suitable_maps": suitable_maps,
                "tips": tips,
                "video_url": video_url,
                "notes": notes,
                "creator_id": st.session_state.user_id,
                "created_at": datetime.now().isoformat(),
                "is_public": True,
                "status": "pending"  # For moderation
            }
            
            if save_build_order(build_order, st.session_state.user_id):
                st.success("Build order submitted successfully! It will be reviewed by our team.")
                # Clear the steps from session state
                st.session_state.build_order_steps = []
                st.rerun()
            else:
                st.error("Failed to submit build order. Please try again.")

def display_user_submissions():
    """Display the user's submitted build orders."""
    if "user_id" not in st.session_state:
        st.warning("Please log in to view your submissions.")
        return
    
    st.subheader("Your Submitted Build Orders")
    
    # Get user's build orders
    build_orders = get_user_build_orders(st.session_state.user_id)
    
    if not build_orders:
        st.info("You haven't submitted any build orders yet.")
        return
    
    # Display build orders
    for bo in build_orders:
        with st.expander(bo["name"]):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(bo["description"])
                st.write(f"**Type:** {bo['type']}")
                st.write(f"**Difficulty:** {bo['difficulty']}")
                st.write(f"**Primary Goal:** {bo['primary_goal']}")
                st.write(f"**Execution Time:** {bo['execution_time']}")
                
                st.write("**Resource Allocation:**")
                for resource, vills in bo["resource_allocation"].items():
                    st.write(f"- {resource.capitalize()}: {vills} villagers")
                
                st.write("**Steps:**")
                for i, step in enumerate(bo["steps"], 1):
                    st.write(f"{i}. {step}")
                
                if bo["tips"]:
                    st.write("**Tips:**")
                    st.write(bo["tips"])
                
                if bo["video_url"]:
                    st.write("**Video Tutorial:**")
                    st.write(bo["video_url"])
                
                if bo["notes"]:
                    st.write("**Additional Notes:**")
                    st.write(bo["notes"])
            
            with col2:
                st.write(f"**Status:** {bo.get('status', 'pending')}")
                st.write(f"**Submitted:** {bo['created_at']}")
                if bo.get("status") == "rejected":
                    st.error("This build order was rejected. Please check the feedback and submit a revised version.") 