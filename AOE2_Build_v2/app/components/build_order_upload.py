import streamlit as st
import json
import os
from datetime import datetime
from app.utils.database import save_build_order, get_user_build_orders, update_build_order, share_build_order

def save_build_order_to_db(build_order, user_id):
    """Save a build order to the database."""
    if "user_id" not in st.session_state:
        st.error("Please log in to save build orders.")
        return False
    
    # Add metadata
    build_order["id"] = f"bo_{datetime.now().timestamp()}"
    build_order["created_at"] = datetime.now().isoformat()
    build_order["creator"] = user_id
    
    try:
        save_build_order(build_order, user_id)
        return True
    except Exception as e:
        st.error(f"Error saving build order: {str(e)}")
        return False

def display_build_order_upload():
    """Display the build order upload form."""
    if "user_id" not in st.session_state:
        st.warning("Please log in to upload build orders.")
        return None
    
    st.subheader("Upload Your Build Order")
    
    with st.form("build_order_upload"):
        name = st.text_input("Build Order Name")
        description = st.text_area("Description")
        build_type = st.selectbox("Build Type", ["Fast Castle", "Scout Rush", "Archer Rush", "Other"])
        difficulty = st.select_slider("Difficulty", options=["Beginner", "Intermediate", "Advanced"])
        primary_goal = st.text_input("Primary Goal")
        execution_time = st.text_input("Execution Time (e.g., '12-14 minutes')")
        
        # Resource allocation
        st.subheader("Resource Allocation")
        col1, col2 = st.columns(2)
        with col1:
            food_vills = st.number_input("Food Villagers", min_value=0, max_value=100, value=0)
            wood_vills = st.number_input("Wood Villagers", min_value=0, max_value=100, value=0)
        with col2:
            gold_vills = st.number_input("Gold Villagers", min_value=0, max_value=100, value=0)
            stone_vills = st.number_input("Stone Villagers", min_value=0, max_value=100, value=0)
        
        # Build order steps
        st.subheader("Build Order Steps")
        steps = []
        for i in range(10):  # Allow up to 10 steps
            step = st.text_input(f"Step {i+1}", key=f"step_{i}")
            if step:
                steps.append(step)
        
        # Additional details
        st.subheader("Additional Details")
        ideal_civs = st.multiselect("Ideal Civilizations", ["All"] + [civ["name"] for civ in st.session_state.get("civilizations", [])])
        suitable_maps = st.multiselect("Suitable Maps", ["All"] + [map["name"] for map in st.session_state.get("maps", [])])
        tips = st.text_area("Tips and Tricks")
        is_public = st.checkbox("Make this build order public")
        
        if st.form_submit_button("Save Build Order"):
            if not name:
                st.error("Please provide a name for your build order.")
                return None
            
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
                "steps": steps,
                "ideal_civilizations": ideal_civs,
                "suitable_maps": suitable_maps,
                "tips": tips,
                "is_public": is_public
            }
            
            if save_build_order_to_db(build_order, st.session_state.user_id):
                st.success(f"Build order '{name}' saved successfully!")
                return build_order
    
    return None

def display_personal_repository():
    """Display the user's personal build order repository."""
    if "user_id" not in st.session_state:
        st.warning("Please log in to view your repository.")
        return
    
    st.subheader("Your Build Order Repository")
    
    # Get user's build orders
    build_orders = get_user_build_orders(st.session_state.user_id)
    
    if not build_orders:
        st.info("You haven't uploaded any build orders yet.")
        return
    
    # Display build orders in a grid
    for bo in build_orders:
        with st.expander(bo["name"]):
            col1, col2, col3 = st.columns([2, 1, 1])
            
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
            
            with col2:
                if st.button("Edit", key=f"edit_{bo['id']}"):
                    st.session_state.editing_build_order = bo
                    st.experimental_rerun()
            
            with col3:
                if st.button("Delete", key=f"delete_{bo['id']}"):
                    if update_build_order(bo["id"], {"deleted": True}, st.session_state.user_id):
                        st.success("Build order deleted!")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to delete build order.")
            
            # Share build order
            st.write("---")
            with st.form(f"share_{bo['id']}"):
                share_email = st.text_input("Share with (email)")
                if st.form_submit_button("Share"):
                    success, message = share_build_order(bo["id"], share_email, st.session_state.user_id)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

def display_build_order_edit(build_order):
    """Display the build order edit form."""
    if "user_id" not in st.session_state:
        st.warning("Please log in to edit build orders.")
        return
    
    st.subheader("Edit Build Order")
    
    with st.form("build_order_edit"):
        name = st.text_input("Build Order Name", value=build_order["name"])
        description = st.text_area("Description", value=build_order["description"])
        build_type = st.selectbox("Build Type", ["Fast Castle", "Scout Rush", "Archer Rush", "Other"], 
                                index=["Fast Castle", "Scout Rush", "Archer Rush", "Other"].index(build_order["type"]))
        difficulty = st.select_slider("Difficulty", options=["Beginner", "Intermediate", "Advanced"],
                                    value=build_order["difficulty"])
        primary_goal = st.text_input("Primary Goal", value=build_order["primary_goal"])
        execution_time = st.text_input("Execution Time", value=build_order["execution_time"])
        
        # Resource allocation
        st.subheader("Resource Allocation")
        col1, col2 = st.columns(2)
        with col1:
            food_vills = st.number_input("Food Villagers", min_value=0, max_value=100, 
                                       value=build_order["resource_allocation"]["food"])
            wood_vills = st.number_input("Wood Villagers", min_value=0, max_value=100,
                                       value=build_order["resource_allocation"]["wood"])
        with col2:
            gold_vills = st.number_input("Gold Villagers", min_value=0, max_value=100,
                                       value=build_order["resource_allocation"]["gold"])
            stone_vills = st.number_input("Stone Villagers", min_value=0, max_value=100,
                                        value=build_order["resource_allocation"]["stone"])
        
        # Build order steps
        st.subheader("Build Order Steps")
        steps = []
        for i in range(10):
            step = st.text_input(f"Step {i+1}", 
                               value=build_order["steps"][i] if i < len(build_order["steps"]) else "",
                               key=f"step_{i}")
            if step:
                steps.append(step)
        
        # Additional details
        st.subheader("Additional Details")
        ideal_civs = st.multiselect("Ideal Civilizations", 
                                  ["All"] + [civ["name"] for civ in st.session_state.get("civilizations", [])],
                                  default=build_order["ideal_civilizations"])
        suitable_maps = st.multiselect("Suitable Maps",
                                     ["All"] + [map["name"] for map in st.session_state.get("maps", [])],
                                     default=build_order["suitable_maps"])
        tips = st.text_area("Tips and Tricks", value=build_order["tips"])
        is_public = st.checkbox("Make this build order public", value=build_order.get("is_public", False))
        
        if st.form_submit_button("Update Build Order"):
            updates = {
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
                "steps": steps,
                "ideal_civilizations": ideal_civs,
                "suitable_maps": suitable_maps,
                "tips": tips,
                "is_public": is_public
            }
            
            if update_build_order(build_order["id"], updates, st.session_state.user_id):
                st.success("Build order updated successfully!")
                del st.session_state.editing_build_order
                st.experimental_rerun()
            else:
                st.error("Failed to update build order.") 