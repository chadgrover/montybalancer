import os

from http.server import HTTPServer, BaseHTTPRequestHandler

host_name = os.environ.get('BE_HOST_NAME', 'localhost')
port = int(os.environ.get('BE_PORT', 8080))

class BackendServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-type", "plain/text")
        self.end_headers()

        level_1 = f"Received request from {self.client_address}"
        level_2 = f"GET / {self.protocol_version}"
        level_3 = f"Host: {self.headers['Host']}"
        level_4 = f"User-Agent: {self.headers['User-Agent']}"
        level_5 = f"Accept: {self.headers['Accept']}"
        level_6 = "Replied with a 200 OK response"

        print(f"./be\n{level_1}\n{level_2}\n{level_3}\n{level_4}\n{level_5}\n{level_6}")

        return

if __name__ == '__main__':
    web_server = HTTPServer((host_name, port), BackendServer)
    print(f"Backend Server started at http://%s:%s" % (host_name, port))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Backend Server stopped.")