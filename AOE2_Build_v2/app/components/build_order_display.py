import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def display_build_order_list(build_orders, compact=False):
    """
    Display a list of build orders as cards.
    
    Args:
        build_orders (list): List of build order dictionaries
        compact (bool): Whether to use a compact display
    
    Returns:
        dict or None: Selected build order or None if none selected
    """
    if not build_orders:
        st.info("No build orders available.")
        return None
    
    # Create a container for the build orders
    container = st.container()
    
    # If compact display, use 3 columns
    if compact:
        cols_per_row = 3
    else:
        cols_per_row = 2
    
    # Group build orders into rows
    rows = [build_orders[i:i + cols_per_row] for i in range(0, len(build_orders), cols_per_row)]
    
    selected_build = None
    
    with container:
        for row in rows:
            cols = st.columns(cols_per_row)
            
            for i, build in enumerate(row):
                with cols[i]:
                    card = st.container()
                    
                    # Header
                    card.subheader(build["name"])
                    
                    # Meta information
                    card.caption(f"Type: {build['type']} | Difficulty: {build['difficulty']}")
                    
                    # Description (shortened for compact view)
                    if compact:
                        description = build["description"][:100] + "..." if len(build["description"]) > 100 else build["description"]
                        card.write(description)
                    else:
                        card.write(build["description"])
                    
                    # Show meta relevance as a progress bar
                    if not compact:
                        col1, col2 = card.columns(2)
                        with col1:
                            st.write("Meta Relevance:")
                        with col2:
                            st.progress(build["meta_relevance"] / 10)
                    
                    # Ideal civilizations
                    if not compact and "ideal_civilizations_names" in build:
                        card.write(f"Ideal Civilizations: {', '.join(build['ideal_civilizations_names'])}")
                    
                    # View button
                    if card.button("View Details", key=f"view_{build['id']}"):
                        selected_build = build
    
    return selected_build

def display_build_order_detail(build_order):
    """
    Display detailed information about a build order.
    
    Args:
        build_order (dict): Build order dictionary
    """
    if not build_order:
        st.warning("No build order selected.")
        return
    
    # Create expander for build order details
    with st.expander("Build Order Overview", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(build_order["name"])
            st.write(build_order["description"])
            
            # Meta information
            st.markdown(f"**Type:** {build_order['type']}")
            st.markdown(f"**Difficulty:** {build_order['difficulty']}")
            st.markdown(f"**Primary Goal:** {build_order['primary_goal']}")
            st.markdown(f"**Execution Time:** ~{build_order['execution_time']} minutes")
            
            # Creator information if available
            if "creator" in build_order and build_order["creator"]:
                st.markdown(f"**Creator:** {build_order['creator']}")
        
        with col2:
            # Meta relevance
            st.subheader("Meta Relevance")
            st.progress(build_order["meta_relevance"] / 10)
            st.caption(f"{build_order['meta_relevance']}/10")
            
            # Suitable maps
            st.subheader("Suitable Maps")
            for map_name in build_order.get("suitable_maps", []):
                st.markdown(f"- {map_name}")
            
            # Ideal civilizations
            st.subheader("Ideal Civilizations")
            for civ_name in build_order.get("ideal_civilizations_names", []):
                st.markdown(f"- {civ_name}")
    
    # Display matchup information
    with st.expander("Matchup Information"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Strong Against")
            for archetype in build_order.get("strong_against", []):
                st.markdown(f"- {archetype}")
        
        with col2:
            st.subheader("Weak Against")
            for archetype in build_order.get("weak_against", []):
                st.markdown(f"- {archetype}")
    
    # Display build order steps
    st.subheader("Build Order Steps")
    
    # Get the steps
    steps = build_order.get("steps", [])
    
    if not steps:
        st.info("No detailed steps available for this build order.")
        return
    
    # Display steps as a table
    steps_df = pd.DataFrame([
        {
            "Step": step["step_number"],
            "Pop": step["population"],
            "Age": step["age"],
            "Time": step.get("time_marker", ""),
            "Action": step["action"],
            "Details": step["description"],
            "Key Point": "⭐" if step.get("key_point", False) else ""
        }
        for step in steps
    ])
    
    # Add highlighting to key steps
    def highlight_key_points(row):
        if row["Key Point"] == "⭐":
            return ["background-color: #ffffcc"] * len(row)
        return [""] * len(row)
    
    # Display the table with styling
    st.dataframe(steps_df.style.apply(highlight_key_points, axis=1), height=400)
    
    # Display resource visualization
    st.subheader("Resource Allocation")
    
    # Extract villager assignment data from steps
    villager_data = []
    for step in steps:
        if "villager_assignment" in step and step["villager_assignment"]:
            # Time marker or step number as x-axis
            x_value = step.get("time_marker", f"Step {step['step_number']}")
            
            # Add data point for each resource
            for resource, count in step["villager_assignment"].items():
                villager_data.append({
                    "Time": x_value,
                    "Resource": resource.capitalize(),
                    "Villagers": count,
                    "Step": step["step_number"]
                })
    
    if villager_data:
        # Create a DataFrame for plotting
        vdf = pd.DataFrame(villager_data)
        
        # Sort by step number to ensure correct order
        vdf = vdf.sort_values("Step")
        
        # Create area chart
        fig = px.area(
            vdf, 
            x="Time", 
            y="Villagers", 
            color="Resource",
            title="Villager Distribution Over Time",
            color_discrete_map={
                "Food": "#FF0000",
                "Wood": "#008000",
                "Gold": "#FFD700",
                "Stone": "#A9A9A9",
                "Idle": "#A0A0A0"
            }
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No resource distribution data available for this build order.")
    
    # Variations section
    if "variations" in build_order and build_order["variations"]:
        st.subheader("Build Order Variations")
        
        for i, variation in enumerate(build_order["variations"]):
            with st.expander(f"Variation {i+1}: {variation.get('name', 'Unnamed Variation')}"):
                st.write(variation.get("description", "No description available."))
                
                if "steps" in variation:
                    st.markdown("### Key Changes")
                    for step in variation["steps"]:
                        st.markdown(f"- **Step {step['step_number']}:** {step['description']}")
    
    # Video tutorials section
    if "video_tutorials" in build_order and build_order["video_tutorials"]:
        st.subheader("Video Tutorials")
        
        for video in build_order["video_tutorials"]:
            st.markdown(f"- [{video.get('title', 'Video Tutorial')}]({video.get('url', '#')})")
    
    # Tips and notes section
    if "tips" in build_order and build_order["tips"]:
        st.subheader("Tips & Notes")
        
        for tip in build_order["tips"]:
            st.markdown(f"- {tip}")

def display_resource_visualization(villager_assignments):
    """
    Display resource allocation visualization.
    
    Args:
        villager_assignments (list): List of villager assignment dictionaries
    """
    if not villager_assignments:
        st.info("No resource distribution data available.")
        return
    
    # Create a DataFrame from the villager assignments
    data = []
    
    for i, assignment in enumerate(villager_assignments):
        time = assignment.get("time", f"Step {i+1}")
        
        for resource, count in assignment["distribution"].items():
            data.append({
                "Time": time,
                "Resource": resource.capitalize(),
                "Villagers": count
            })
    
    df = pd.DataFrame(data)
    
    # Create an area chart
    fig = px.area(
        df,
        x="Time",
        y="Villagers",
        color="Resource",
        title="Villager Distribution Over Time",
        color_discrete_map={
            "Food": "#FF0000",
            "Wood": "#008000",
            "Gold": "#FFD700",
            "Stone": "#A9A9A9"
        }
    )
    
    st.plotly_chart(fig, use_container_width=True) 