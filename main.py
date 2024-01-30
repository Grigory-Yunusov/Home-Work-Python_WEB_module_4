from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import json
import socket
import threading

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        print(data)
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        print(data_dict)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

def run_http(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


UDP_IP = '127.0.0.1'
UDP_PORT = 5000


def run_server(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        server = ip, port
        sock.bind(server)
        try:
            while True:
                data, address = sock.recvfrom(1024)
                print(f"Received data: {data.decode()} to server: {server}")
                data_dict = json.loads(data.decode())
                with open('storage/data.json', 'a') as file:
                    json.dump(data_dict, file, indent=2)
                sock.sendto(data, address)
                print(f"Sent data: {data.decode()} to: {address}")
        except KeyboardInterrupt:
            print(f'Destroy server')
            raise
        finally:
            print('Closing server socket')

if __name__ == '__main__':
    socket_server = threading.Thread(target=run_server, args=(UDP_IP, UDP_PORT))
    http_server = threading.Thread(target=run_http) # ось тут потріббно аргумент передавати??????

    socket_server.start()
    http_server.start()
    socket_server.join()
    http_server.join()
    print('Done!')