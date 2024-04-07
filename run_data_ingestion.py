import time
import schedule
import subprocess
from datetime import datetime

def run_script():

    # Set the time between the script will work
    start_time = datetime.strptime("07:00", "%H:%M").time()
    stop_time = datetime.strptime("23:00", "%H:%M").time()
    current_time = datetime.now().time()

    print(f"Request time: {str(current_time).split('.')[0]}")

    # Run the script between 7:00 and 23:00
    if (start_time <= current_time) and (stop_time >= current_time):
        subprocess.run(["python", "code/data_ingestion.py"])

# Schedule the task every 3 minutes between 7:00 and 23:00
schedule.every(180).seconds.do(run_script)

while True:
    # Run the task
    schedule.run_pending()
    # Stop the bucle 1 second before run again the task
    time.sleep(1)   

