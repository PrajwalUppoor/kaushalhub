import os
import sqlite3
from datetime import datetime

DB_PATH = "mentorship.db"
MIGRATIONS_DIR = "migrations"

def run_migrations():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure migration history table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS migration_history (
            version TEXT PRIMARY KEY,
            applied_on TEXT
        )
    """)
    conn.commit()

    applied = {row[0] for row in cursor.execute("SELECT version FROM migration_history")}
    files = sorted(f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql"))

    for file in files:
        version = file.split(".")[0]
        if version not in applied:
            print(f"🛠️ Applying migration: {file}")
            with open(os.path.join(MIGRATIONS_DIR, file), "r") as f:
                sql = f.read()
                cursor.executescript(sql)
                cursor.execute("INSERT INTO migration_history (version, applied_on) VALUES (?, ?)",
                               (version, datetime.now().isoformat()))
                conn.commit()
    conn.close()
    print("✅ All migrations applied.")