import os
import sys
import subprocess
import signal

# Run with python3 run_servers.py 8080 8081 8082

PROCESSES = []

def kill_processes(sig, frame):
    for process in PROCESSES:
        process.kill()
    sys.exit(0)

signal.signal(signal.SIGINT, kill_processes)

if len(sys.argv) > 1:
    ports = [str(port) for port in sys.argv[1:]]
    os.environ["BE_PORTS"] = " ".join(ports)

    for port in ports:
        process = subprocess.Popen(["python3", "-m", "http.server", port, "--directory", "./static",])
        PROCESSES.append(process)

else:
    os.environ["BE_PORTS"] = "8080"
    process = subprocess.Popen(["python3", "-m", "http.server", "8080", "--directory", "./static",])
    PROCESSES.append(process)

process = subprocess.Popen(["python3", "lb.py",])
PROCESSES.append(process)

