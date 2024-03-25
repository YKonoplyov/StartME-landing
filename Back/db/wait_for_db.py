from time import sleep
import subprocess
from sqlalchemy import text
from engine import sync_engine


def wait_for_db() -> None:
    while True:
        try:
            print("trying to connect ...")
            subprocess.run(["alembic", "upgrade", "head"])
            with sync_engine.connect() as db:
                checked = db.execute(text("SELECT * FROM funds"))
                print("Connected")
                break
        except Exception as e:
            print("Waiting for db ...")
            sleep(5)

if __name__ == "__main__":
    wait_for_db()