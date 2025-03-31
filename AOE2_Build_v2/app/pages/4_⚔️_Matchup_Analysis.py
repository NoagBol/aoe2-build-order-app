import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.civilization_selector import display_civilization_multiselect
from utils.data_loader import load_civilizations, load_matchup_data
from utils.matchup_calculator import calculate_team_matchup, get_counter_strategies
from utils.recommendation_engine import get_recommended_build_orders
from components.build_order_display import display_build_order_list

def display_matchup_heatmap(matchup_matrix, civilization_names):
    """Display a heatmap of matchup win rates."""
    fig = go.Figure(data=go.Heatmap(
        z=matchup_matrix,
        x=civilization_names,
        y=civilization_names,
        colorscale='RdBu_r',  # Red-Blue scale (red = bad, blue = good)
        zmin=35,  # Min win rate
        zmax=65,  # Max win rate
        zmid=50,  # 50% is neutral
        colorbar=dict(
            title="Win Rate %",
            titleside="right"
        )
    ))
    
    fig.update_layout(
        title="Civilization Matchup Win Rates",
        xaxis_title="Enemy Civilization",
        yaxis_title="Your Civilization",
        height=600,
        width=800
    )
    
    st.plotly_chart(fig)

def main():
    st.set_page_config(
        page_title="Civilization Matchup Analysis",
        page_icon="⚔️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("Civilization Matchup Analysis")
    
    # Select analysis type
    analysis_type = st.radio(
        "Analysis Type",
        ["1v1 Matchup", "Team Analysis", "Counter Picker"]
    )
    
    civilizations = load_civilizations()
    
    if analysis_type == "1v1 Matchup":
        # 1v1 matchup analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Your Civilization")
            your_civ = display_civilization_multiselect(civilizations, max_selections=1, key="your_civ")
        
        with col2:
            st.subheader("Opponent Civilization")
            opponent_civ = display_civilization_multiselect(civilizations, max_selections=1, key="opponent_civ")
        
        if your_civ and opponent_civ:
            # Load matchup data
            matchup_data = load_matchup_data(your_civ[0]["id"], opponent_civ[0]["id"])
            
            if matchup_data:
                st.header(f"{your_civ[0]['name']} vs {opponent_civ[0]['name']}")
                
                # Display win rate and advantage
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        label="Win Rate", 
                        value=f"{matchup_data['win_rate']:.1f}%",
                        delta=f"{(matchup_data['win_rate'] - 50):.1f}%"
                    )
                with col2:
                    st.metric(
                        label="Advantage", 
                        value=matchup_data["advantage_level"]
                    )
                
                # Key factors in the matchup
                st.subheader("Key Matchup Factors")
                for factor in matchup_data["key_factors"]:
                    st.markdown(f"- {factor}")
                
                # Counter strategies
                st.subheader("Recommended Counter Strategies")
                for strategy in matchup_data["counter_strategies"]:
                    st.markdown(f"- {strategy}")
                
                # Recommended build orders
                st.subheader("Recommended Build Orders")
                recommended_builds = get_recommended_build_orders(
                    civilization_id=your_civ[0]["id"],
                    enemy_civs=[opponent_civ[0]["name"]]
                )
                display_build_order_list(recommended_builds, compact=True)
            else:
                st.warning("No specific matchup data available for these civilizations.")
    
    elif analysis_type == "Team Analysis":
        # Team analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Your Team")
            your_team = display_civilization_multiselect(civilizations, max_selections=4, key="your_team")
        
        with col2:
            st.subheader("Enemy Team")
            enemy_team = display_civilization_multiselect(civilizations, max_selections=4, key="enemy_team")
        
        if your_team and enemy_team:
            # Calculate team matchup
            team_analysis = calculate_team_matchup(your_team, enemy_team)
            
            # Display team synergy
            st.header("Team Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Your Team Synergy")
                st.progress(team_analysis["your_team_synergy"] / 10)
                st.write(f"Synergy Score: {team_analysis['your_team_synergy']}/10")
                
                st.subheader("Team Strengths")
                for strength in team_analysis["your_team_strengths"]:
                    st.markdown(f"- {strength}")
            
            with col2:
                st.subheader("Enemy Team Synergy")
                st.progress(team_analysis["enemy_team_synergy"] / 10)
                st.write(f"Synergy Score: {team_analysis['enemy_team_synergy']}/10")
                
                st.subheader("Enemy Team Strengths")
                for strength in team_analysis["enemy_team_strengths"]:
                    st.markdown(f"- {strength}")
            
            # Overall matchup assessment
            st.subheader("Matchup Assessment")
            st.write(team_analysis["overall_assessment"])
            
            # Recommended team strategies
            st.subheader("Recommended Team Strategies")
            for strategy in team_analysis["recommended_strategies"]:
                st.markdown(f"- {strategy}")
    
    elif analysis_type == "Counter Picker":
        # Counter picker tool
        st.subheader("Select Enemy Civilization(s)")
        enemy_civs = display_civilization_multiselect(civilizations, max_selections=None, key="enemies_to_counter")
        
        if enemy_civs:
            # Get counter civilizations
            counter_civs = get_counter_strategies(enemy_civs)
            
            st.header("Recommended Counter Civilizations")
            
            # Display counter civilizations as a grid
            counter_grid = [counter_civs[i:i+3] for i in range(0, len(counter_civs), 3)]
            for row in counter_grid:
                cols = st.columns(3)
                for i, civ in enumerate(row):
                    with cols[i]:
                        if "icon_path" in civ and civ["icon_path"]:
                            st.image(civ["icon_path"], width=80)
                        st.subheader(civ["name"])
                        st.write(f"Counter Score: {civ['counter_score']}/10")
                        st.write(f"**Why?** {civ['counter_reason']}")

            # Display overall matchup heatmap
            if st.checkbox("Show Matchup Heatmap"):
                st.subheader("Matchup Win Rate Heatmap")
                st.info("This heatmap shows win rates between civilizations. Blue indicates favorable matchups (>50% win rate), red indicates unfavorable matchups (<50% win rate).")
                
                # In a real implementation, this would be loaded from a database
                # Here we'll simulate a random matchup matrix
                selected_civ_names = [civ["name"] for civ in enemy_civs]
                n_civs = len(selected_civ_names)
                
                # Create a dummy matchup matrix for demonstration
                np.random.seed(42)  # For reproducible results
                matchup_matrix = np.random.normal(50, 5, (n_civs, n_civs))
                np.fill_diagonal(matchup_matrix, 50)  # Diagonal is always 50%
                
                display_matchup_heatmap(matchup_matrix, selected_civ_names)

if __name__ == "__main__":
    main() 