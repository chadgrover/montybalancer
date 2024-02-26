import os
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

LB_HOST_NAME = os.environ.get('LB_HOST_NAME', 'localhost')
LB_PORT = int(os.environ.get('LB_PORT', 8000))
BE_HOST_NAME = os.environ.get('BE_HOST_NAME', 'localhost')
BE_PORT = int(os.environ.get('BE_PORT', 8081))

class MontyBalancer(BaseHTTPRequestHandler):
    def do_GET(self):
        response = requests.get("http://%s:%s" % (BE_HOST_NAME, BE_PORT))

        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-type", "plain/text")
        self.end_headers()

        level_1 = f"Received request from {self.client_address}"
        level_2 = f"GET / {self.protocol_version}"
        level_3 = f"Host: {self.headers['Host']}"
        level_4 = f"User-Agent: {self.headers['User-Agent']}"
        level_5 = f"Accept: {self.headers['Accept']}"

        print(f"./lb\n{level_1}\n{level_2}\n{level_3}\n{level_4}\n{level_5}")
        print(f"Response from Backend Server: {response.status_code}")

        return

if __name__ == '__main__':
    web_server = HTTPServer((LB_HOST_NAME, LB_PORT), MontyBalancer)
    print(f"MontyBalancer has started at http://%s:%s" % (LB_HOST_NAME, LB_PORT))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("MontyBalancer stopped.")