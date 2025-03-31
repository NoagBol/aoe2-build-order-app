import streamlit as st
import hashlib
from app.utils.database import get_user, create_user, init_db
import sqlite3

def show_profile_page():
    """Display the user profile page."""
    st.title("User Profile")
    
    # Initialize database if needed
    init_db()
    
    # Check if user is logged in
    if "user_id" not in st.session_state:
        st.warning("Please log in to view your profile.")
        show_login_form()
        return
    
    # Get user data
    user = get_user(st.session_state.user_id)
    if not user:
        st.error("User not found.")
        return
    
    # Display profile information
    st.subheader("Profile Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Username:** {user[1]}")
        st.write(f"**Email:** {user[2]}")
        st.write(f"**Member since:** {user[6]}")
    
    with col2:
        if user[4]:  # AoE2 username exists
            st.write(f"**AoE2 Username:** {user[4]}")
            st.write(f"**Platform:** {user[5]}")
        else:
            st.info("No AoE2 account connected")
    
    # AoE2 Account Connection
    st.subheader("Connect AoE2 Account")
    with st.form("aoe2_connection"):
        aoe2_username = st.text_input("AoE2 Username")
        aoe2_platform = st.selectbox("Platform", ["Steam", "Microsoft Store", "Other"])
        
        if st.form_submit_button("Connect Account"):
            # Here you would typically verify the AoE2 account
            # For now, we'll just update the database
            conn = sqlite3.connect(get_db_path())
            c = conn.cursor()
            c.execute('''
                UPDATE users 
                SET aoe2_username = ?, aoe2_platform = ?
                WHERE id = ?
            ''', (aoe2_username, aoe2_platform, user[0]))
            conn.commit()
            conn.close()
            st.success("AoE2 account connected successfully!")
            st.rerun()
    
    # Change Password
    st.subheader("Change Password")
    with st.form("change_password"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        if st.form_submit_button("Change Password"):
            if new_password != confirm_password:
                st.error("New passwords do not match!")
            else:
                # Verify current password
                current_hash = hashlib.sha256(current_password.encode()).hexdigest()
                if current_hash != user[3]:
                    st.error("Current password is incorrect!")
                else:
                    # Update password
                    new_hash = hashlib.sha256(new_password.encode()).hexdigest()
                    conn = sqlite3.connect(get_db_path())
                    c = conn.cursor()
                    c.execute('''
                        UPDATE users 
                        SET password_hash = ?
                        WHERE id = ?
                    ''', (new_hash, user[0]))
                    conn.commit()
                    conn.close()
                    st.success("Password updated successfully!")

def show_login_form():
    """Display the login form."""
    st.subheader("Login")
    with st.form("login"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            # Here you would verify credentials against the database
            # For now, we'll just create a new user if they don't exist
            conn = sqlite3.connect(get_db_path())
            c = conn.cursor()
            c.execute('SELECT id FROM users WHERE email = ?', (email,))
            user = c.fetchone()
            
            if not user:
                # Create new user
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                user_id = create_user(email.split('@')[0], email, password_hash)
                st.session_state.user_id = user_id
                st.success("Account created and logged in!")
                st.rerun()
            else:
                # Verify password
                c.execute('SELECT password_hash FROM users WHERE id = ?', (user[0],))
                stored_hash = c.fetchone()[0]
                if stored_hash == hashlib.sha256(password.encode()).hexdigest():
                    st.session_state.user_id = user[0]
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid password!")
            
            conn.close() 