# gmail_utils.py

import os
import pickle
import base64
import streamlit as st
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes: Permission to send email on user's behalf
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_PATH = "token.pickle"


def get_gmail_service():
    creds = None

    # Try to load token from file (already authorized)
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    # If no valid token, perform OAuth login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config({
                "installed": {
                    "client_id": st.secrets["google"]["client_id"],
                    "client_secret": st.secrets["google"]["client_secret"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            }, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the token for next time
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def send_email(to, subject, body):
    service = get_gmail_service()

    message = EmailMessage()
    message.set_content(body)
    message["To"] = to
    message["From"] = "me"
    message["Subject"] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_message = {'raw': raw_message}

    try:
        message = service.users().messages().send(userId="me", body=send_message).execute()
        st.success("📧 Email sent successfully!")
        return message
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")
        return None


# Example usage in Streamlit (uncomment to test):
# if st.button("Send Test Email"):
#     send_email("recipient@example.com", "Hello from KaushalHub", "This is a test email.")
