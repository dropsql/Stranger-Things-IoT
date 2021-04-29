# ipv4scan -n 500 | python3 ipv4scan_connect.py

import sys
import json

from core.database import Database

from lib.logging import Logging

database = Database()

for line in sys.stdin:
    json_data = json.loads(line)
    database.add_server(
        host=json_data['ip'],
        port=json_data['port'],
        headers_lines=json_data['headers'].split('\r\n'),
    )

    Logging.print_success(f'added {json_data["ip"]}:{json_data["port"]} to the database')