# mentorship_tracker_app/auth.py

import streamlit as st
import sqlite3
import bcrypt

DB_PATH = "mentorship.db"

def create_user_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('mentor', 'mentee')) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user():
    st.subheader("📝 Register")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("I am a:", ["mentor", "mentee"])

    if st.button("Register"):
        if not (name and email and password):
            st.warning("Please fill all fields.")
            return

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                           (name, email, hashed_pw, role))
            conn.commit()
            conn.close()
            st.success("Registration successful! Please login.")
        except sqlite3.IntegrityError:
            st.error("This email is already registered.")

def login_user():
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, password, role FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()

        if row and bcrypt.checkpw(password.encode(), row[1].encode()):
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.user_id = row[0]
            st.session_state.user_role = row[2]
        else:
            st.error("Invalid email or password.")

def get_user_role(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    role = cursor.fetchone()
    conn.close()
    return role[0] if role else None

# Create table on module import
create_user_table()
