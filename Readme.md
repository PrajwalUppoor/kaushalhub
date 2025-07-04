# 🚀 KaushalHub - Mentorship Tracker

**KaushalHub** is a secure and scalable mentorship platform built using Streamlit, allowing mentors and mentees to collaborate efficiently, track skill development, assign and monitor tasks, and communicate seamlessly across engineering domains.

> *"Shaping the All-in-One Engineer"*

---

## 🌟 Features

### 👩‍🏫 For Mentors:
- Assign and review tasks for mentees
- Track mentee progress across multiple skills/domains
- Schedule 1:1 sessions via Google Calendar integration
- Push blogs, mentorship roadmaps, and curated learning materials
- WebSocket-based messaging and real-time notifications
- Manage profile, expertise, and availability (calendar)

### 👨‍🎓 For Mentees:
- Submit tasks and progress updates
- Request mentor meetings with calendar availability check
- Browse mentor profiles and mentorship fields
- View published content, notifications, and deadlines
- Receive automated updates via Email/WhatsApp
- Secure file upload (resume, assignments)

### 🛠 Admin Dashboard:
- Manage users (mentors & mentees)
- View logs and activity reports
- Trigger safe rebuilds with backup/migration
- Export system data (CSV/Excel)
- Monitor application health and feature rollout

---

## 🔐 Authentication & Security

- Role-based login (mentor, mentee, admin)
- Encrypted passwords with hashed storage
- Gmail SSO (OAuth 2.0) login available
- Defenses against SQL Injection, XSS, and CSRF
- Rebuild-safe flags for database migration/versioning
- Safe trigger deployment with test-gated workflows

---

## 🧱 Tech Stack

| Layer          | Tools Used                          |
|----------------|--------------------------------------|
| UI & Backend   | Streamlit (Python)                   |
| Auth           | Custom + Google OAuth                |
| DB             | SQLite with auto-migration support   |
| Messaging      | WebSocket for in-app chat            |
| Email/Alerts   | Gmail API + Discord + WhatsApp API   |
| DevOps         | GitHub Actions CI/CD                 |
| Reporting      | CSV/Excel Export + Logs              |

---

## 🧪 Tests & CI

- Pytest-based unit test suite
- GitHub Actions for CI/CD
- Discord alerts on failure
- Auto-trigger rebuilds only if tests pass

---
