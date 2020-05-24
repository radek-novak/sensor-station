#! python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BufferedIOBase
import sqlite3
import os
import time
import random
import string


db_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'sensors.db'))


def randomword(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def init():
    with open('setup.sql') as f:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.executescript(f.read())

        connection.commit()
        connection.close()


def execute(command, data=None):
    # 20ms - 1400ms
    # start = time.perf_counter()

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    if data is None:
        cursor.execute(command)
    else:
        cursor.executemany(command, data)

    connection.commit()
    connection.close()

    # print(f"took {time.perf_counter() - start}s")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response_only(200, 'OK')
        self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        post_body = self.rfile.read(
            int(self.headers['content-length']))

        split = post_body.decode("utf-8").split('|')

        if len(split) == 3:
            execute("insert into Sensors values (?, ?, ?)", [tuple(split)])

        self.wfile.write(post_body)


def main(port=8000):
    print('Initializing db')
    init()

    server_address = ('', port)
    httpd = HTTPServer(server_address, Handler)
    print(f'Starting server on port {port}')
    httpd.serve_forever()


if __name__ == "__main__":
    main(8000)
