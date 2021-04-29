import hashlib

from typing import List

class Hashing:
    @staticmethod
    def make_headers_hash(port: int, headers: List[str]) -> str:
        return hashlib.sha1(
            str(port).encode() + \
            b';'.join([
                x.encode()
                for x in headers
            ])
        ).hexdigest()