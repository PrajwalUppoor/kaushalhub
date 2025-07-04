# mentorship_tracker_app/pages/admin_dashboard.py

import streamlit as st
import sqlite3
import pandas as pd
import shutil
import os
from datetime import datetime

DB_PATH = "mentorship.db"
BACKUP_DIR = "backups"
LOG_FILE = "streamlit_app.log"
AUDIT_FILE = "admin_audit.log"

# ---------------------------- AUTH ----------------------------
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.title("🔐 Admin Login")
    admin_user = st.text_input("Username")
    admin_pass = st.text_input("Password", type="password")
    if st.button("Login"):
        if admin_user == "admin" and admin_pass == "kaushalhub@123":
            st.session_state.admin_logged_in = True
            st.experimental_rerun()
        else:
            st.error("❌ Invalid credentials")
    st.stop()

# ---------------------------- ADMIN DASHBOARD ----------------------------
st.title("🔧 Admin Dashboard - KaushalHub")
st.markdown("This panel allows full control and monitoring of the platform.")

os.makedirs(BACKUP_DIR, exist_ok=True)
conn = sqlite3.connect(DB_PATH)

# Tabs with export buttons
tabs = st.tabs([
    "All Users", "Mentor-Mentee Map", "Tasks", "Progress Logs", "Calendar Logs", "System Logs", "Backup", "Restore DB", "Audit Trail", "Safe Rebuild"])

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = tabs

# ---------------------------- TAB 1: All Users ----------------------------
with tab1:
    st.markdown("### 👥 All Registered Users")
    users = pd.read_sql_query("SELECT id, name, email, role FROM users", conn)
    st.dataframe(users, use_container_width=True)
    st.download_button("📤 Export Users", users.to_csv(index=False).encode(), "users.csv")

# ---------------------------- TAB 2: Mappings ----------------------------
with tab2:
    st.markdown("### 🔗 Mentor-Mentee Mappings")
    query = """
        SELECT m.name AS mentee, mt.name AS mentor
        FROM mentor_mentee mm
        JOIN users m ON mm.mentee_id = m.id
        JOIN users mt ON mm.mentor_id = mt.id
    """
    mappings = pd.read_sql_query(query, conn)
    st.dataframe(mappings, use_container_width=True)
    st.download_button("📤 Export Mappings", mappings.to_csv(index=False).encode(), "mappings.csv")

# ---------------------------- TAB 3: Tasks ----------------------------
with tab3:
    st.markdown("### 📋 All Assigned Tasks")
    query = """
        SELECT t.id, u.name AS mentee, t.title, t.due_date, t.status
        FROM tasks t
        JOIN users u ON t.mentee_id = u.id
    """
    tasks = pd.read_sql_query(query, conn)
    st.dataframe(tasks, use_container_width=True)
    st.download_button("📤 Export Tasks", tasks.to_csv(index=False).encode(), "tasks.csv")

# ---------------------------- TAB 4: Progress Logs ----------------------------
with tab4:
    st.markdown("### 📈 Task Progress Updates")
    query = """
        SELECT u.name AS mentee, t.title, p.update, p.timestamp
        FROM progress_updates p
        JOIN users u ON p.mentee_id = u.id
        JOIN tasks t ON p.task_id = t.id
    """
    logs = pd.read_sql_query(query, conn)
    st.dataframe(logs, use_container_width=True)
    st.download_button("📤 Export Progress Logs", logs.to_csv(index=False).encode(), "progress_logs.csv")

# ---------------------------- TAB 5: Calendar Logs ----------------------------
with tab5:
    st.markdown("### 📅 Calendar Scheduling (Debug)")
    st.info("This section will display real-time booking logs in production.")
    st.write("[TODO]: Hook into event logs or webhook callbacks if enabled")

# ---------------------------- TAB 6: System Logs ----------------------------
with tab6:
    st.markdown("### 🛠️ System & App Logs")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = f.read()
            st.text_area("📄 Streamlit Logs", logs, height=300)
    else:
        st.info("No log file found.")

# ---------------------------- TAB 7: Backup DB ----------------------------
with tab7:
    st.markdown("### 💾 Database Backup")
    if st.button("📥 Take Backup of DB"):
        backup_file = os.path.join(BACKUP_DIR, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
        shutil.copy(DB_PATH, backup_file)
        with open(backup_file, "rb") as f:
            st.download_button("📥 Download Backup File", f.read(), os.path.basename(backup_file))
        st.success("✅ Backup created and ready for download!")

# ---------------------------- TAB 8: Restore DB ----------------------------
with tab8:
    st.markdown("### ♻️ Restore Database From Backup")
    uploaded = st.file_uploader("Upload a .db backup file", type="db")
    if uploaded:
        with open("mentorship.db", "wb") as f:
            f.write(uploaded.read())
        st.success("✅ Database restored successfully. Please refresh the page.")

# ---------------------------- TAB 9: Audit Trail ----------------------------
with tab9:
    st.markdown("### 🕵️ Admin Audit Trail")
    if os.path.exists(AUDIT_FILE):
        with open(AUDIT_FILE, "r") as f:
            logs = f.read()
            st.text_area("Audit Logs", logs, height=300)
    else:
        st.info("Audit trail not available. Start logging admin actions to 'admin_audit.log'.")

# ---------------------------- TAB 10: Safe Rebuild ----------------------------
with tab10:
    st.markdown("### 🧱 Safe Rebuild or Upgrade")
    st.warning("This will back up the DB and allow restart/update without losing data.")

    if st.button("🧱 Backup and Mark for Rebuild"):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(BACKUP_DIR, f"auto_rebuild_backup_{timestamp}.db")
        shutil.copy(DB_PATH, backup_file)

        with open("rebuild.flag", "w") as f:
            f.write(f"Triggered at {timestamp}")

        st.success("✅ Safe rebuild marked. Please restart Streamlit manually or wait for auto-deploy!")

conn.close()
