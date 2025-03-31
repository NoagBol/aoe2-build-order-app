import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_civilization_statistics, load_build_order_statistics

def display_civilization_win_rates(civ_stats):
    """Display civilization win rate statistics."""
    # Sort by win rate
    sorted_stats = sorted(civ_stats, key=lambda x: x["win_rate"], reverse=True)
    
    # Create DataFrame for visualization
    df = pd.DataFrame([
        {
            "Civilization": civ["name"],
            "Win Rate": civ["win_rate"],
            "Pick Rate": civ["pick_rate"],
            "Specialty": civ["primary_specialty"]
        }
        for civ in sorted_stats
    ])
    
    # Create win rate bar chart
    fig = px.bar(
        df, 
        x="Civilization", 
        y="Win Rate",
        color="Win Rate",
        color_continuous_scale="RdBu",
        labels={"Win Rate": "Win Rate (%)"},
        title="Civilization Win Rates",
        hover_data=["Pick Rate", "Specialty"]
    )
    
    # Mark 50% win rate with a horizontal line
    fig.add_shape(
        type="line",
        x0=-0.5,
        y0=50,
        x1=len(df) - 0.5,
        y1=50,
        line=dict(color="black", dash="dash"),
    )
    
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

def display_build_order_stats(build_stats):
    """Display build order success statistics."""
    if not build_stats:
        st.info("No build order statistics available.")
        return
    
    # Create DataFrame for visualization
    df = pd.DataFrame([
        {
            "Build Order": build["name"],
            "Success Rate": build["success_rate"],
            "Popularity": build["popularity"],
            "Type": build["type"],
            "Difficulty": build["difficulty"]
        }
        for build in build_stats
    ])
    
    # Filter options
    build_types = ["All"] + sorted(df["Type"].unique().tolist())
    selected_type = st.selectbox("Filter by Build Type", build_types)
    
    if selected_type != "All":
        df = df[df["Type"] == selected_type]
    
    # Sort options
    sort_options = {
        "Success Rate (High to Low)": ("Success Rate", False),
        "Success Rate (Low to High)": ("Success Rate", True),
        "Popularity (High to Low)": ("Popularity", False),
        "Popularity (Low to High)": ("Popularity", True)
    }
    
    selected_sort = st.selectbox("Sort by", list(sort_options.keys()))
    sort_column, ascending = sort_options[selected_sort]
    df = df.sort_values(by=sort_column, ascending=ascending)
    
    # Create visualization
    fig = px.bar(
        df,
        x="Build Order",
        y="Success Rate",
        color="Difficulty",
        hover_data=["Popularity", "Type"],
        title="Build Order Success Rates",
        labels={"Success Rate": "Success Rate (%)"}
    )
    
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

def display_meta_trends():
    """Display meta trends over time."""
    # Simulated data for civilization popularity over time
    civilizations = ["Franks", "Britons", "Aztecs", "Chinese", "Magyars"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    
    # Create a DataFrame with random data (in a real app, this would come from a database)
    import numpy as np
    np.random.seed(42)
    
    data = []
    for civ in civilizations:
        # Start with a base value and add some randomness with a trend
        base = np.random.randint(5, 15)
        trend = np.random.choice([-1, 1]) * np.random.uniform(0.2, 0.5)
        
        for i, month in enumerate(months):
            value = max(1, min(20, base + trend * i + np.random.normal(0, 1)))
            data.append({"Civilization": civ, "Month": month, "Pick Rate": value})
    
    df = pd.DataFrame(data)
    
    # Create line chart for meta trends
    fig = px.line(
        df,
        x="Month",
        y="Pick Rate",
        color="Civilization",
        title="Civilization Popularity Over Time",
        labels={"Pick Rate": "Pick Rate (%)"}
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def display_pro_player_stats():
    """Display professional player strategies and statistics."""
    # Simulated data for pro player preferred civilizations
    pro_players = {
        "TheViper": ["Mayans", "Chinese", "Huns", "Franks", "Aztecs"],
        "Liereyy": ["Mayans", "Britons", "Ethiopians", "Franks", "Lithuanians"],
        "Hera": ["Chinese", "Mayans", "Aztecs", "Franks", "Indians"],
        "TaToH": ["Byzantines", "Mongols", "Malay", "Chinese", "Huns"],
        "DauT": ["Byzantines", "Persians", "Teutons", "Chinese", "Malians"]
    }
    
    # Create DataFrame for visualization
    data = []
    for player, civs in pro_players.items():
        for i, civ in enumerate(civs):
            data.append({
                "Player": player,
                "Civilization": civ,
                "Preference Rank": i + 1
            })
    
    df = pd.DataFrame(data)
    
    # Create heatmap for pro player preferences
    pivot_df = df.pivot(index="Player", columns="Civilization", values="Preference Rank")
    pivot_df = pivot_df.fillna(6)  # Fill NA with a value higher than max rank
    
    # Sort columns by total preference (lower is better)
    col_sums = pivot_df.sum()
    sorted_cols = col_sums.sort_values().index
    pivot_df = pivot_df[sorted_cols]
    
    fig = px.imshow(
        pivot_df,
        color_continuous_scale="Viridis_r",  # reversed so dark is more preferred
        labels=dict(x="Civilization", y="Player", color="Preference Rank"),
        title="Pro Player Civilization Preferences (Lower Rank = More Preferred)",
        aspect="auto"
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(
        page_title="Statistics & Meta Analysis",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("Age of Empires II: Statistics & Meta Analysis")
    
    # Tab selection
    tab1, tab2, tab3, tab4 = st.tabs([
        "Civilization Stats", 
        "Build Order Stats", 
        "Meta Analysis", 
        "Pro Strategies"
    ])
    
    with tab1:
        st.header("Civilization Statistics")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            elo_range = st.selectbox(
                "ELO Range",
                ["All", "<1000", "1000-1200", "1200-1400", "1400-1600", "1600-1800", "1800-2000", "2000+"]
            )
        with col2:
            patch_version = st.selectbox(
                "Game Version",
                ["Latest Patch", "Update 101.102.3476.0", "Update 100.100.3425.0"]
            )
        with col3:
            map_filter = st.selectbox(
                "Map",
                ["All Maps", "Arabia", "Arena", "Islands", "Black Forest", "Nomad"]
            )
        
        # Load civilization statistics
        civ_stats = load_civilization_statistics(
            elo_range="All" if elo_range == "All" else elo_range,
            patch_version=None if patch_version == "Latest Patch" else patch_version,
            map_type=None if map_filter == "All Maps" else map_filter
        )
        
        if civ_stats:
            display_civilization_win_rates(civ_stats)
        else:
            st.info("No civilization statistics available for the selected filters.")
    
    with tab2:
        st.header("Build Order Statistics")
        
        # Load build order statistics
        build_stats = load_build_order_statistics()
        
        if build_stats:
            display_build_order_stats(build_stats)
        else:
            st.info("No build order statistics available.")
    
    with tab3:
        st.header("Meta Analysis")
        
        st.subheader("Civilization Popularity Trends")
        display_meta_trends()
        
        st.subheader("Current Meta Overview")
        st.write("""
        The current meta heavily favors aggressive Feudal Age strategies, particularly on open maps.
        Civilizations with strong economic bonuses like Chinese and Mayans remain top tier, while
        Cavalry civilizations like Franks and Lithuanians are consistently strong across different maps.
        """)
        
        st.write("""
        Recent balance changes have slightly reduced the dominance of Gurjaras, though they remain
        a strong choice. The slight buff to Infantry has made Goths and Vikings more viable in the 
        late game, especially on closed maps.
        """)
    
    with tab4:
        st.header("Professional Player Strategies")
        
        st.subheader("Pro Player Civilization Preferences")
        display_pro_player_stats()
        
        st.subheader("Tournament Trends")
        st.write("""
        In recent tournaments, we've seen a shift towards more aggressive Feudal Age strategies,
        with many pro players opting for civilizations with strong archer rushes. The map pool
        has significantly influenced civilization picks, with water maps bringing Italians and
        Portuguese back into the meta.
        """)
        
        st.subheader("Build Orders from Recent Tournaments")
        st.info("This feature will be available in the next update.")

if __name__ == "__main__":
    main() 