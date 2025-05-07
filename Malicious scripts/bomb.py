import os
import time

# Path to monitor
monitor_path = "C:\\Users\\TrentonUser\\Downloads\\vmVulnerableWeb\\keylogger.py"

# Function to delete files if monitor file is deleted
def self_destruct():
    files_to_delete = [
        "C:\\Users\\TrentonUser\\Downloads\\vmVulnerableWeb\\vmMySecWeb.py",
        "C:\\Users\\TrentonUser\\Downloads\\vmVulnerableWeb\\vm_vulnerable.db",
        "C:\\Users\\TrentonUser\\Downloads\\vmVulnerableWeb\\bomb.py", # Add more file paths as needed
    ]
    for file in files_to_delete:
        try:
            os.remove(file)
            print(f"{file} deleted.")
        except FileNotFoundError:
            print(f"{file} not found.")

# Monitor the file periodically
while True:
    if not os.path.exists(monitor_path):
        print("Monitor file not found. Executing self-destruct.")
        self_destruct()
        break
    time.sleep(60)  # Check every minute