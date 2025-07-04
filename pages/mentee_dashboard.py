# mentorship_tracker_app/pages/mentee_dashboard.py

import streamlit as st
import sqlite3
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pytz

DB_PATH = "mentorship.db"

# ---------------------------- Google Calendar Integration ----------------------------
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "credentials/your_service_account.json"  # Replace with your file

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
calendar_service = build("calendar", "v3", credentials=credentials)
CALENDAR_ID = "primary"  # or the mentor's calendar ID

def request_meeting_with_mentor(mentee_id, mentor_email, selected_date, selected_time):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM users WHERE id = ?", (mentee_id,))
    mentee = cursor.fetchone()
    conn.close()

    mentee_name, mentee_email = mentee
    datetime_str = f"{selected_date} {selected_time}"
    local_dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    local_tz = pytz.timezone("Asia/Kolkata")
    local_dt = local_tz.localize(local_dt)
    start = local_dt.isoformat()
    end = (local_dt + timedelta(hours=1)).isoformat()

    event = {
        'summary': f"Mentorship Session: {mentee_name}",
        'description': f"Requested by {mentee_name} ({mentee_email})",
        'start': {'dateTime': start, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end, 'timeZone': 'Asia/Kolkata'},
        'attendees': [{'email': mentor_email}, {'email': mentee_email}],
    }
    calendar_service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    st.success("📨 Meeting request submitted to calendar!")

def mentee_dashboard(user_id):
    st.subheader("🙋‍♂️ Mentee Dashboard")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tab1, tab2, tab3, tab4 = st.tabs(["My Tasks", "Submit Progress", "Mentor Profiles", "Schedule Session"])

    # ---------------------------- TAB 1: My Tasks ----------------------------
    with tab1:
        st.markdown("### 📌 Assigned Tasks")
        cursor.execute("""
            SELECT id, title, description, due_date, status FROM tasks
            WHERE mentee_id = ?
        """, (user_id,))
        tasks = cursor.fetchall()
        if tasks:
            for t in tasks:
                st.markdown(f"**{t[1]}** (Due: {t[3]})\nStatus: {t[4]}\n\n{t[2]}")
        else:
            st.info("No tasks assigned yet.")

    # ---------------------------- TAB 2: Submit Progress ----------------------------
    with tab2:
        st.markdown("### 📝 Submit Progress Update")
        cursor.execute("SELECT id, title FROM tasks WHERE mentee_id = ?", (user_id,))
        task_list = cursor.fetchall()
        if task_list:
            task_dict = {f"{t[1]} (ID: {t[0]})": t[0] for t in task_list}
            selected_task = st.selectbox("Select Task", list(task_dict.keys()))
            progress = st.text_area("Update")
            if st.button("Submit Update"):
                cursor.execute("""
                    INSERT INTO progress_updates (mentee_id, task_id, update, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (user_id, task_dict[selected_task], progress, datetime.now().isoformat()))
                conn.commit()
                st.success("✅ Progress updated!")
        else:
            st.info("No tasks to update yet.")

    # ---------------------------- TAB 3: Mentor Profiles ----------------------------
    with tab3:
        st.markdown("### 👨‍🏫 View Mentor Profiles")

        filter_skill = st.text_input("🔍 Filter by Skill")

        query = """
            SELECT u.id, u.name, u.email, p.role, p.company, p.skills, p.about, p.profile_pic
            FROM users u
            JOIN mentor_profiles p ON u.id = p.user_id
            WHERE u.role = 'mentor'
        """
        cursor.execute(query)
        mentors = cursor.fetchall()

        if filter_skill:
            mentors = [m for m in mentors if filter_skill.lower() in m[5].lower()]

        if mentors:
            for mentor_id, name, email, role, company, skills, about, profile_pic in mentors:
                with st.container():
                    cols = st.columns([1, 4])
                    with cols[0]:
                        if profile_pic:
                            st.image(profile_pic, width=100)
                        else:
                            st.image("https://via.placeholder.com/100", width=100)
                    with cols[1]:
                        st.markdown(f"**{name}**  ")
                        st.markdown(f"*{role} at {company}*  ")
                        st.markdown(f"📧 {email}")
                        st.markdown(f"💡 **Skills**: {skills}")
                        st.markdown(f"📝 {about}")

                        with st.expander("📅 Request Meeting"):
                            selected_date = st.date_input(f"Date for {name}", key=f"date_{mentor_id}")
                            selected_time = st.time_input(f"Time (24H) for {name}", key=f"time_{mentor_id}")
                            if st.button(f"Send Request to {name}", key=f"send_{mentor_id}"):
                                request_meeting_with_mentor(user_id, email, selected_date, selected_time.strftime("%H:%M"))
        else:
            st.info("No mentor profiles found.")

    # ---------------------------- TAB 4: Schedule Session ----------------------------
    with tab4:
        st.markdown("### 📅 Schedule Time With Mentor")
        st.info("This will show Google Calendar slots once calendar integration is completed.")

    conn.close()
