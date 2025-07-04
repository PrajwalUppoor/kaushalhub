import os
import shutil
import sqlite3
from datetime import datetime
from utils.migrate import run_migrations

DB_PATH = "mentorship.db"
REBUILD_FLAG = "rebuild.flag"
BACKUP_DIR = "backups"
CACHE_FILE = "cache/templates.cache"  # optional if used

def backup_database():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"mentorship_backup_{timestamp}.db")
    shutil.copy(DB_PATH, backup_path)
    print(f"🛡️ Database backed up to {backup_path}")

def clear_caches():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        print("🧹 Cleared cached templates.")

def handle_rebuild():
    if os.path.exists(REBUILD_FLAG):
        print("🚨 Detected rebuild.flag - triggering rebuild process...")

        with open(REBUILD_FLAG) as f:
            reason = f.read()
            print("🔄 Rebuild Reason:", reason)

        backup_database()
        run_migrations()
        clear_caches()

        os.remove(REBUILD_FLAG)
        print("✅ Rebuild complete. Flag removed.")
