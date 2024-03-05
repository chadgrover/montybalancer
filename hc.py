import os
import requests
import sys
from utils.set_interval import set_interval
from urllib.parse import urlparse

LB_PORT = os.environ.get("LB_PORT", 8001)
LB_URL = f"http://localhost:{LB_PORT}/"

# Run with python3 hc.py <url> <interval_in_seconds>

if len(sys.argv) == 3:
    url = str(sys.argv[1])
    listening_port = urlparse(url).port
    removed_from_list = False

    def make_get_request():
        global removed_from_list
        
        response = requests.get(url)

        if response.status_code == 200 and removed_from_list is True:
            requests.post(LB_URL, data={"port": listening_port})
            removed_from_list = False

        elif response.status_code != 200 and removed_from_list is False:
            requests.delete(LB_URL, data={"port": listening_port})
            removed_from_list = True
        else:
            pass

    interval_in_seconds = int(sys.argv[2])
    set_interval(make_get_request, interval_in_seconds)

else:
    print("Not enough arguments given.")

