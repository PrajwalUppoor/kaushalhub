# mentorship_tracker_app/pages/mentor_dashboard.py

import streamlit as st
import sqlite3
from datetime import datetime
from gmail.gmail_utils import send_email
from google_calendar.calendar_utils import get_authenticated_service, create_event, get_mentor_busy_slots

DB_PATH = "mentorship.db"

def mentor_dashboard(user_id):
    st.subheader("👩‍🏫 Mentor Dashboard")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Assign Tasks", "Analytics", "Resources", "Activity Log", "Mentor-Mentee Mapping", "Schedule Meeting"])

    # ---------------------------- TAB 6: Schedule Meeting ----------------------------
    with tab6:
        st.markdown("### 📅 Schedule Meetings or Set Availability")

        credentials = get_authenticated_service(user_id)
        if credentials:
            st.success("✅ Google Calendar Authenticated")

            action = st.radio("Choose Action", ["Create Meeting with Mentee", "Block Time Slot"])

            if action == "Create Meeting with Mentee":
                cursor.execute("""
                    SELECT u.id, u.name, u.email FROM users u
                    JOIN mentor_mentee mm ON mm.mentee_id = u.id
                    WHERE mm.mentor_id = ?
                """, (user_id,))
                mentees = cursor.fetchall()

                if mentees:
                    mentee_map = {f"{m[1]} ({m[2]})": (m[0], m[2]) for m in mentees}
                    selected_label = st.selectbox("Select Mentee to Invite", list(mentee_map.keys()))
                    mentee_id, mentee_email = mentee_map[selected_label]

                    title = st.text_input("Event Title")
                    description = st.text_area("Agenda")
                    start = st.datetime_input("Start Time")
                    end = st.datetime_input("End Time")

                    busy_slots = get_mentor_busy_slots(credentials, start.date(), end.date())
                    conflict = any(bs['start'] <= start.isoformat() <= bs['end'] or
                                   bs['start'] <= end.isoformat() <= bs['end'] for bs in busy_slots)

                    if conflict:
                        st.warning("⚠️ The selected time overlaps with your busy calendar slots.")
                    else:
                        if st.button("📨 Send Calendar Invite"):
                            create_event(
                                credentials=credentials,
                                summary=title,
                                description=description,
                                start=start,
                                end=end,
                                attendees=[mentee_email]
                            )
                            st.success("✅ Invite sent via Google Calendar!")
                else:
                    st.info("No mentees mapped to you yet.")

            elif action == "Block Time Slot":
                st.markdown("Mark a personal busy slot in your calendar")
                title = st.text_input("Busy Slot Title")
                start = st.datetime_input("Start Time")
                end = st.datetime_input("End Time")

                if st.button("🕒 Mark as Busy"):
                    create_event(
                        credentials=credentials,
                        summary=title or "Busy",
                        description="Unavailable",
                        start=start,
                        end=end,
                        attendees=[]
                    )
                    st.success("✅ Busy slot added to calendar")
        else:
            st.warning("Please authenticate with Google to use calendar features.")

    # ---------------------------- TAB 5: Mentor-Mentee Mapping ----------------------------
    with tab5:
        st.markdown("### 🔗 Manage Mentor-Mentee Mapping")
        cursor.execute("SELECT id, name FROM users WHERE role = 'mentor'")
        mentors = cursor.fetchall()
        cursor.execute("SELECT id, name FROM users WHERE role = 'mentee'")
        mentees = cursor.fetchall()

        mentor_map = {m[1]: m[0] for m in mentors}
        mentee_map = {m[1]: m[0] for m in mentees}

        selected_mentor = st.selectbox("Select Mentor", list(mentor_map.keys()))
        selected_mentee = st.selectbox("Select Mentee", list(mentee_map.keys()))

        if st.button("Map Mentee to Mentor"):
            cursor.execute("INSERT OR REPLACE INTO mentor_mentee (mentee_id, mentor_id) VALUES (?, ?)",
                           (mentee_map[selected_mentee], mentor_map[selected_mentor]))
            conn.commit()
            st.success(f"✅ {selected_mentee} is now mapped to {selected_mentor}")

        st.markdown("### 🔍 Existing Mappings")
        cursor.execute("""
            SELECT m.name as mentee, mt.name as mentor
            FROM mentor_mentee mm
            JOIN users m ON mm.mentee_id = m.id
            JOIN users mt ON mm.mentor_id = mt.id
        """)
        mappings = cursor.fetchall()
        if mappings:
            st.dataframe(mappings, use_container_width=True)
        else:
            st.info("No mappings found.")
