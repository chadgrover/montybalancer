import os
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

LB_HOST_NAME = os.environ.get('LB_HOST_NAME', 'localhost')
LB_PORT = int(os.environ.get('LB_PORT', 8001))

BE_HOST_NAME = os.environ.get('BE_HOST_NAME', 'localhost')
BE_PORTS = os.environ.get('BE_PORTS').split(' ')
SERVERS_LIST = [int(port) for port in BE_PORTS]

current_server = None
HTTPServer.allow_reuse_address = True

class MontyBalancer(BaseHTTPRequestHandler):

    # A static method is a method that doesn't require access to the instance or class.
    @staticmethod
    def round_robin(servers_list):
        cached_servers_list = servers_list
        i = 0

        def increment_and_return_next_server():
            # Allows i to be modified in the closure
            nonlocal i

            result = cached_servers_list[i]
            i = (i + 1) % len(cached_servers_list)

            return result
        
        return increment_and_return_next_server

    def do_GET(self):
        current_port = current_server()
        
        response = requests.get("http://%s:%s" % (BE_HOST_NAME, current_port))

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
        print(f"Response from server running at {response.url}\nStatus Code: {response.status_code}")

        return

if __name__ == '__main__':
    current_server = MontyBalancer.round_robin(SERVERS_LIST)
    web_server = HTTPServer((LB_HOST_NAME, LB_PORT), MontyBalancer)
    print(f"MontyBalancer has started at http://%s:%s" % (LB_HOST_NAME, LB_PORT))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...\n")
    except Exception as e:
        print("Error:\n")
        print(e)

    web_server.shutdown()
    web_server.server_close()

    print("MontyBalancer stopped.")