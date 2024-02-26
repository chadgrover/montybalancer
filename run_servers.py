import sys
import subprocess

# Run with python3 run_servers.py <port>

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        PORT = str(arg)
        subprocess.Popen(["python3", "-m", "http.server", PORT, "--directory", "./static",])
else:
    subprocess.Popen(["python3", "-m", "http.server", "8000", "--directory", "./static",])

