import hashlib
import hmac
import time

import httpx


class RakutenAuth(httpx.Auth):
    def __init__(self, key: str, sercret: str):
        self.key = key
        self.sercret = sercret.encode()

    def auth_flow(self, request: httpx.Request):
        nonce = str(int(time.time() * 1000))

        string = nonce.encode()
        if request.method in {"GET", "DELETE"}:
            string += request.url.raw_path
        elif request.method in {"POST", "PUT"}:
            string += request.content

        signature = hmac.new(self.sercret, string, hashlib.sha256).hexdigest()

        request.headers["API-KEY"] = self.key
        request.headers["NONCE"] = nonce
        request.headers["SIGNATURE"] = signature

        yield request
