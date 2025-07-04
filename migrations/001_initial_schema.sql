CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT
);

CREATE TABLE IF NOT EXISTS mentor_profiles (
    user_id INTEGER PRIMARY KEY,
    role TEXT,
    company TEXT,
    skills TEXT,
    about TEXT,
    profile_pic TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS mentees (
    user_id INTEGER PRIMARY KEY,
    branch TEXT,
    college TEXT,
    phone TEXT,
    current_role TEXT,
    domain TEXT,
    skills TEXT,
    resume_path TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mentor_id INTEGER,
    mentee_id INTEGER,
    title TEXT,
    description TEXT,
    due_date TEXT,
    status TEXT
);

CREATE TABLE IF NOT EXISTS progress_updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mentee_id INTEGER,
    task_id INTEGER,
    update TEXT,
    timestamp TEXT
);

CREATE TABLE IF NOT EXISTS mentor_blog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mentor_id INTEGER,
    title TEXT,
    content TEXT,
    published_on TEXT
);

CREATE TABLE IF NOT EXISTS referrals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mentee_id INTEGER,
    company TEXT,
    role TEXT,
    status TEXT
);

CREATE TABLE IF NOT EXISTS migration_history (
    version TEXT PRIMARY KEY,
    applied_on TEXT
);
