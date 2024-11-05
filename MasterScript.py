#!/usr/bin/env python3
import subprocess, time, psutil
from datetime import datetime
def run_sub():
    #Checks to see if subprocess is active
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if "python" in proc.info['name'] and '/home/hayden/Downloads/FaceRec.py' in proc.info['cmdline']:
            print("Subprocess is already running.")
            return
    #If subprocess not running, start the subprocess
    result = subprocess.Popen(["python", '/home/hayden/Downloads/FaceRec.py'])
    print(f"Started subprocess with PID: {result.pid}")
occur_once = True
reset_time = None
run_sub()

try:
    while True:
        current_time = datetime.now().strftime("%H:%M")
        if current_time == "00:01" and occur_once == True:
            run_sub()
            occur_once = False
            reset_time = datetime.now()
        if current_time == "00:00" and reset_time:
            occur_once = True
            reset_time = None
        time.sleep(1)
except KeyboardInterrupt:
    pass
print("MASTERSCRIPT CLOSING...")