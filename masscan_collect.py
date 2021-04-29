# /!\ output file must be from "-oL output_file" argument!
#
#
# masscan --port=80 --banners -oL scan.txt --rate=50000 164.132.0.0/16
# can scan.txt | py masscan_collect.py

import sys
import re

from core.database import Database

database = Database()

pattern = r'banner tcp (?P<port>\d{1,5}) (?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \d+ http (?P<headers>.*)'

for line in sys.stdin:
    match = re.match(pattern, line.strip())
    if match:
        host = match.group('host')
        port = match.group('port')

        headers = match.group('headers')

        headers_lines = headers.split('\\x0d\\x0a')[:-1]
        print(headers_lines)

        database.add_server(host, port, headers_lines)