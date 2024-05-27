from http.server import HTTPServer,BaseHTTPRequestHandler
import time

host = "192.168.1.87"
port = 3000

class NeutralHttp(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes('<html><head><title>Neutral</title></head><body><h1>Neutrals</h1></body></html>','utf-8'))

server = HTTPServer((host,port),NeutralHttp)
print("Server started")

server.serve_forever()
server.server_close()

print("server closed")