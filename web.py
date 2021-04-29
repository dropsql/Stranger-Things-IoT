from flask import Flask, render_template, request

from core.database import Database

from lib.hashing import Hashing
from lib.logging import Logging

from rich.console import Console

HOST = '127.0.0.1'
PORT = 1337

app = Flask(__name__, static_url_path='')

console = Console(
    record=True
)

@app.route('/', methods=['GET']) # TODO: html input
def root_GET():
    query = request.args.get('q', '')
    if query:
        db = Database()
        results = db.search_query(query)
        hosts = {
            Hashing.make_headers_hash(port, headers): []
            for _, port, headers in results
        }

        for ip, port, headers in results:
            hosts[Hashing.make_headers_hash(port, headers)].append((ip, port, headers))

        for _hash, reports in hosts.items():
            _hosts = [ip for ip, port, headers in reports]
            table = Logging.render_host_table(
                '\n'.join(_hosts),
                str(port),
                headers
            )
            console.print(table)
        return console.export_html()

app.run(host=HOST, port=PORT, threaded=True)