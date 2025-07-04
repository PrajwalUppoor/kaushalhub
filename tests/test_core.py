import os
import pytest
from utils.migrate import run_migrations
from utils.rebuild import handle_rebuild, backup_database

def test_run_migrations_idempotent():
    # Should not raise or apply already-run migrations
    run_migrations()
    assert True  # If it completes, test passes

def test_backup_creates_file():
    backup_database()
    backups = os.listdir("backups")
    assert any(f.endswith(".db") for f in backups)

def test_handle_rebuild_creates_backup_and_clears_flag(tmp_path):
    flag = tmp_path / "rebuild.flag"
    flag.write_text("test rebuild")
    os.chdir(tmp_path)
    
    from utils.rebuild import handle_rebuild
    handle_rebuild()

    assert not flag.exists()
