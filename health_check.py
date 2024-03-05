import sys
import requests
from threading import Timer

# Run with python3 health_check.py <URL> <Timeout>

def set_interval(callback, seconds):
    def wrapper():
        set_interval(callback, seconds)
        callback()

    t = Timer(seconds, wrapper)
    t.start()
    return t

if len(sys.argv) == 3:
    url = str(sys.argv[1])
    interval_in_seconds = int(sys.argv[2])

    def make_get_request():
        requests.get(url)

    set_interval(make_get_request, interval_in_seconds)

else:
    print("Not enough arguments given.")