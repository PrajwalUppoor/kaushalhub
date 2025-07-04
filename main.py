# mentorship_tracker_app/main.py

import streamlit as st
import os
from auth import login_user, register_user, get_user_role
from pages.mentor_dashboard import mentor_dashboard
from pages.mentee_dashboard import mentee_dashboard
from utils.migrate import run_migrations
from utils.rebuild import handle_rebuild

# ---------------- Run DB Migrations + Safe Rebuild ----------------
run_migrations()
handle_rebuild()

# ---------------- Page Config ----------------
st.set_page_config(page_title="KaushalHub - Mentorship Tracker", layout="wide")

# ---------------- Branding ----------------
st.markdown("""
<div style='text-align: center; padding: 1rem 0;'>
    <h1 style='color: #1f77b4;'>🚀 KaushalHub</h1>
    <h4 style='color: #444;'>Shaping the All-in-One Engineer</h4>
    <p style='max-width: 800px; margin: 0 auto; font-size: 16px;'>
        A secure, scalable mentorship platform to track progress, assign tasks, schedule sessions, and build collaborative engineering skills across domains like Full Stack, DevOps, AI/ML, Embedded, Product, VLSI, Cloud and more.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- Session State ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_id = None

# ---------------- Main App Logic ----------------
if not st.session_state.logged_in:
    auth_option = st.sidebar.radio("Login/Register", ["Login", "Register"])
    if auth_option == "Login":
        login_user()
    else:
        register_user()
else:
    if st.session_state.user_role == "mentor":
        mentor_dashboard(st.session_state.user_id)
    elif st.session_state.user_role == "mentee":
        mentee_dashboard(st.session_state.user_id)

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.user_id = None
        st.success("Logged out successfully.")
