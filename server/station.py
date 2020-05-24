#! python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BufferedIOBase
from datetime import datetime
import sqlite3
import os
import time
import random
import string
import json


db_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'sensors.db'))
db_sql_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'setup.sql'))
id_len = 8
port = 8000

sensor_name_cache = {}


def gen_id():
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(id_len))


def init():
    with open(db_sql_path) as f:
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
        cursor.execute(command, data)

    connection.commit()
    connection.close()

    # print(f"took {time.perf_counter() - start}s")


def record(data):
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()

    sensor_id = None

    if data['name'] not in sensor_name_cache:
        cur.execute('SELECT id FROM sensors WHERE name=?', (data['name'],))

        fetched_id = cur.fetchone()

        if fetched_id is None:
            cur.execute("INSERT INTO sensors VALUES (?, ?)",
                        (None, data['name']))
            sensor_id = cur.lastrowid
        else:
            sensor_id = fetched_id[0]

        sensor_name_cache[data['name']] = sensor_id
    else:
        sensor_id = sensor_name_cache[data['name']]

    date = datetime.now().astimezone().replace(microsecond=0).isoformat()
    rowdata = [gen_id(), date, sensor_id, data['value']]
    cur.execute("INSERT INTO sensordata VALUES (?, ?, ?, ?)", rowdata)

    connection.commit()
    connection.close()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response_only(200, 'OK')
        self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        post_body = self.rfile.read(
            int(self.headers['content-length']))

        data = json.loads(post_body)
        print(data)
        self.wfile.write(post_body)

        record(data)


def main():
    print('Initializing db')
    init()

    server_address = ('', port)
    httpd = HTTPServer(server_address, Handler)
    print(f'Starting server on port {port}')
    httpd.serve_forever()


if __name__ == "__main__":
    main()
