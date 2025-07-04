# mentorship_tracker_app/google_calendar/calendar_utils.py

import datetime
import os
import streamlit as st
from google.oauth2 import credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from streamlit.runtime.scriptrunner import get_script_run_ctx
from google.auth.transport.requests import Request
import pickle

# Store credentials in session or local cache
def get_authenticated_service(user_id):
    if "google_credentials" not in st.session_state:
        try:
            flow = Flow.from_client_secrets_file(
                "credentials/client_secret.json",
                scopes=["https://www.googleapis.com/auth/calendar"],
                redirect_uri="http://localhost:8501/"
            )
            auth_url, _ = flow.authorization_url(prompt="consent")
            st.markdown(f"[Authorize Google Calendar]({auth_url})")
            return None
        except Exception as e:
            st.error(f"Google Auth Error: {e}")
            return None
    else:
        creds = st.session_state.google_credentials
        return creds

# Create Calendar Event
def create_event(credentials, summary, description, start, end, attendees):
    service = build("calendar", "v3", credentials=credentials)

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': [{'email': email} for email in attendees],
        'reminders': {
            'useDefault': True
        }
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event.get('htmlLink')

# Get Busy Slots from Calendar
def get_mentor_busy_slots(credentials, start_date, end_date):
    service = build("calendar", "v3", credentials=credentials)

    body = {
        "timeMin": datetime.datetime.combine(start_date, datetime.time.min).isoformat() + 'Z',
        "timeMax": datetime.datetime.combine(end_date, datetime.time.max).isoformat() + 'Z',
        "timeZone": "Asia/Kolkata",
        "items": [{"id": "primary"}]
    }

    eventsResult = service.freebusy().query(body=body).execute()
    busy_times = eventsResult['calendars']['primary']['busy']
    return busy_times
