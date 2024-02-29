import os
import sys
import subprocess

# Run with python3 run_servers.py 8080 8081 8082

if len(sys.argv) > 1:
    ports = [str(port) for port in sys.argv[1:]]
    os.environ["BE_PORTS"] = " ".join(ports)

    for port in ports:
        subprocess.Popen(["python3", "-m", "http.server", port, "--directory", "./static",])

else:
    os.environ["BE_PORTS"] = "8080"
    subprocess.Popen(["python3", "-m", "http.server", "8080", "--directory", "./static",])

subprocess.Popen(["python3", "lb.py",])