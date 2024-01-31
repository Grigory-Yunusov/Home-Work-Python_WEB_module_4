from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import json
import socket
import threading
from datetime import datetime
from pathlib import Path
import logging


BUFFER_SIZE = 1024
BASE_DIR = Path()
PORT_HTTP = 3000
HOST_HTTP = "0.0.0.0"
UDP_IP = '127.0.0.1'
UDP_PORT = 5000



class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            file = BASE_DIR.joinpath(pr_url.path[1:])
            if file.exists():
                self.send_static(file)
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        size = self.headers.get('Content-Length')
        data = self.rfile.read(int(size))
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(data, (UDP_IP, UDP_PORT))
        client_socket.close()
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        mime_type, *_ = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header("Content-type", mime_type)
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def run_http_server(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

def run_server_socket(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((host, port))
        logging.info("Starting socket")
        try:
            while True:
                msg, address = sock.recvfrom(BUFFER_SIZE)               
                logging.info("++")
                save_data(msg)
        except KeyboardInterrupt:
            print(f'Destroy server')
            raise
        finally:
            print('Closing server socket')

def save_data(data):
    data_parse = urllib.parse.unquote_plus(data.decode())
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        new_data ={current_time: {key: value for key, value in [el.split("=") for el in data_parse.split("&")]}}
        # new_data = {}                     # без сахара
        # for el in data_parse.split("&"):
        #     key, value = el.split("=")
        #     new_data[current_time] = {key: value}
        file_path = "storage/data.json"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {}

        existing_data.update(new_data)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=2)

    except ValueError as error:
        logging.error(f"ValueError: {error}")
    except OSError as oser:
        logging.error(f"OSError: {oser}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s%(message)s')

    socket_server = threading.Thread(target=run_server_socket, args=(UDP_IP, UDP_PORT))
    http_server = threading.Thread(target=run_http_server, args=(HTTPServer, HttpHandler))

    socket_server.start()
    http_server.start()
    socket_server.join()
    http_server.join()
    print('Done!')