# 📓 Changelog

All notable changes to **KaushalHub** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [1.0.0] - 2025-07-04

### ✨ Added
- Streamlit-based mentorship platform core architecture
- Role-based authentication system for mentors and mentees
- Secure login & registration with password hashing
- Gmail OAuth2 login (SSO)
- SQLite database with migration and version tracking
- Mentor dashboard:
  - Task assignment and tracking per mentee
  - Upload blog posts and mentorship roadmaps
  - View mentee calendar availability
- Mentee dashboard:
  - Task progress view and submission
  - Mentor browsing with skill/domain filters
  - Request meetings via Google Calendar
- Mentor profile upload + display in mentee dashboard
- Google Calendar API integration:
  - Two-way scheduling and availability
  - Invite mentors to events directly
- Gmail API integration:
  - Email alerts for task assignments and submissions
- WebSocket-based in-app messaging between mentor & mentee
- Notification system for unread messages and task updates
- Admin dashboard:
  - View logs, all users, mentor-mentee mapping
  - Export data to CSV/Excel
  - Trigger safe rebuilds with DB backup and migration
- Unit test suite with `pytest`
- GitHub Actions CI workflow:
  - Auto-trigger rebuilds only after passing tests
  - Discord webhook alert on CI failure
- Modular codebase with `auth`, `utils`, `pages`, `database`, `gmail_utils`, and `calendar_utils`
- Branding added: KaushalHub - "Shaping the All-in-One Engineer"

---

## [Unreleased]

### 🔮 Planned
- AI/ML-powered mentor suggestion engine
- Resume screening automation
- Peer feedback and endorsements
- Group mentoring and cohort management
- ChatGPT integration for mentoring Q&A

---
