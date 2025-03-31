import streamlit as st
import sys
import os

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    st.set_page_config(
        page_title="About the Build Order Advisor",
        page_icon="ℹ️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("About the Build Order Advisor")
    
    st.markdown("""
    ## Project Overview
    
    The Age of Empires II: Definitive Edition Build Order Advisor is a sophisticated Streamlit application 
    designed to provide players with expert-level build order recommendations tailored to their specific game 
    circumstances.
    
    Unlike simplistic build order guides, this application takes into account the complex interplay between 
    civilization choice, map type, team compositions, and enemy civilizations to provide contextually relevant 
    strategic recommendations.
    
    ## Features
    
    - **Comprehensive Build Orders**: Detailed step-by-step instructions with timing markers, resource allocation, 
      and strategic tips.
    - **Map Analysis**: In-depth analysis of different map types and their impact on gameplay strategies.
    - **Matchup Analysis**: Statistics and recommendations for civilization matchups in 1v1 and team games.
    - **Counter Strategies**: Suggested civilizations and strategies to counter specific opponent picks.
    - **Statistics & Meta Analysis**: Current meta trends, win rates, and professional player strategies.
    
    ## How It Works
    
    The application uses a combination of expert knowledge, statistical analysis, and strategic heuristics to 
    generate recommendations. The data is regularly updated to reflect the current meta and game balance changes.
    
    ## About the Author
    
    This project was created by a senior software developer and Age of Empires II veteran with over 20 years of 
    gameplay experience. Drawing from thousands of hours of gameplay and meta-analysis, the application serves as 
    both a learning tool for intermediate players and a strategic assistant for advanced players.
    
    ## Version Information
    
    - **Application Version**: 1.0.0
    - **Last Updated**: 2023-11-13
    - **Supported Game Version**: Age of Empires II: Definitive Edition (Latest Patch)
    
    ## Acknowledgements
    
    Special thanks to the Age of Empires II community, professional players, and content creators whose insights 
    and strategies have contributed to this project.
    
    ## Feedback and Contributions
    
    Feedback, bug reports, and contributions are welcome! Please visit the project's GitHub repository to submit 
    issues or pull requests.
    
    ## License
    
    This project is licensed under the MIT License. See the LICENSE file for details.
    """)
    
    st.subheader("Contact Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Email**: example@example.com
        
        **GitHub**: [github.com/example/aoe2-build-advisor](https://github.com/example/aoe2-build-advisor)
        """)
    
    with col2:
        st.markdown("""
        **Twitter**: [@AOE2BuildAdvisor](https://twitter.com/example)
        
        **Discord**: [Join our community](https://discord.gg/example)
        """)
    
    # Disclaimer
    st.subheader("Disclaimer")
    st.markdown("""
    This is an unofficial fan project. Age of Empires II is a registered trademark of Microsoft Corporation. 
    This project is not affiliated with or endorsed by Microsoft Corporation.
    """)

if __name__ == "__main__":
    main() 