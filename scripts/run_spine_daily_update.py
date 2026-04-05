import schedule
import time
import subprocess

def run_update():
    print("Running daily spine update...")
    subprocess.run(["python", "scripts/spine_daily_update.py"], check=True)
    subprocess.run(["git", "add", "reports/"], check=True)
    subprocess.run(["git", "commit", "-m", "docs: generate daily Spine update report"], check=False)
    print("Update complete.")

schedule.every().day.at("00:00").do(run_update)

if __name__ == "__main__":
    print("Scheduler started. Press Ctrl+C to exit.")
    while True:
        schedule.run_pending()
        time.sleep(60)
