CREATE TABLE IF NOT EXISTS meeting_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mentor_email TEXT,
    mentee_email TEXT,
    date TEXT,
    time TEXT,
    calendar_event_id TEXT
);
