import sqlite3
import time
import re

from typing import List

class Database:
    def __init__(self, database_path='database.db'):
        
        self.database = sqlite3.connect(database_path)
        self.cursor = self.database.cursor()
        
        self.init_database()

        super().__init__()

    def regexp(self, query: str, text: str) -> bool:
        """ search function for sqlite """
        return query.lower() in text.lower()

    def save(self) -> None:
        """ save the commits """
        self.database.commit()

    def init_database(self):
        """ init the database """
        queries = [
            'CREATE TABLE IF NOT EXISTS scan    ( time real, host text, port integer );',    # create the table that will contains ip & ports
            'CREATE TABLE IF NOT EXISTS headers ( scan_id integer, line text );',            # create the table that will contains headers

            'CREATE INDEX IF NOT EXISTS idxline on headers ( line );',
            'CREATE INDEX IF NOT EXISTS idxscan on headers ( scan_id );'
        ]

        [self.cursor.execute(query) for query in queries]

        self.database.create_function(
            'regexp',
            2,
            self.regexp
        )

        self.save()

    def add_server(self, host: str, port: int, headers_lines: List[str]):
        """ add a server to the database """
        self.cursor.execute(
            'INSERT INTO scan (time, host, port) VALUES (?, ?, ?);',
            [time.time(), host, port]
        )

        scan_id = self.cursor.lastrowid
        values = []

        [
            values.append((scan_id, header_line)) 
            for header_line in headers_lines
        ]

        self.cursor.executemany(
            'INSERT INTO headers (scan_id, line) VALUES (?, ?);',
            values
        )

        self.save()

    def get_lines(self, scan_id) -> List[str]:
        """ get the headers from the scan id """
        self.cursor.execute(
            'SELECT line FROM headers WHERE scan_id = ? ORDER BY rowid;', 
            [scan_id]
        )

        return [x[0] for x in self.cursor.fetchall()]

    def search_query(self, query: str) -> None:
        """ search a query into the database """
        self.cursor.execute(
            'SELECT headers.scan_id, scan.host, scan.port FROM headers JOIN scan ON scan.rowid = headers.scan_id WHERE line regexp ? GROUP BY headers.scan_id', 
            [query]
        )

        results = []
        for row in self.cursor.fetchall():
            scan_id, host, port = row
            results.append((host, port, self.get_lines(scan_id)))
        
        return results