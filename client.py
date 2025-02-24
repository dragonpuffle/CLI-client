import json
import socket
import base64
from typing import Dict, Self


class HttpRequest:
    def __init__(self, method: str, path: str, headers: Dict[str, str], body: dict = None):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body or {}

    def to_bytes(self) -> bytes:
        body_json = json.dumps(self.body)
        self.headers['Content-Length'] = str(len(body_json))
        headers_str = '\r\n'.join(f'{k}: {v}' for k, v in self.headers.items())

        request = (
            f'{self.method} {self.path} HTTP/1.1\r\n'
            f'{headers_str}\r\n\r\n'
            f'{body_json}'
        )
        return request.encode()

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> Self:
        text = binary_data.decode()
        lines = text.split('\r\n')

        method, path, _ = lines[0].split(' ')
        headers = {}
        body = {}

        i = 1
        while i < len(lines) and lines[i]:
            key, value = lines[i].split(': ', 1)
            headers[key] = value
            i += 1

        if 'Content-Length' in headers:
            body_json = lines[-1]
            body = json.loads(body_json)

        return cls(method, path, headers, body)


class HttpResponse:
    def __init__(self, status_code: int, headers: Dict[str, str], body: dict = None):
        self.status_code = status_code
        self.headers = headers
        self.body = body or {}

    def to_bytes(self) -> bytes:
        body_json = json.dumps(self.body)
        self.headers['Content-Length'] = str(len(body_json))
        headers_str = '\r\n'.join(f'{k}: {v}' for k, v in self.headers.items())

        response = (
            f'{self.status_code} OK\r\n'
            f'{headers_str}\r\n\r\n'
            f'{body_json}'
        )
        return response.encode()

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> Self:
        text = binary_data.decode()
        lines = text.split('\r\n')

        _, status_code, _ = lines[0].split(' ', 2)
        status_code = int(status_code)
        headers = {}
        body = {}

        i = 1
        while i < len(lines) and lines[i]:
            key, value = lines[i].split(': ', 1)
            headers[key] = value
            i += 1

        if 'Content-Length' in headers:
            body_json = lines[-1]
            body = json.loads(body_json)

        return cls(status_code, headers, body)


class HttpClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.host, self.port = self.parse_url(base_url)

    def parse_url(self, url: str):
        parts = url.replace('http://', '').split(':')
        host = parts[0]
        port = int(parts[1])
        return host, port

    def post(self, path: str, body: dict, headers: Dict[str, str]) -> str:
        request = HttpRequest('POST', path, headers, body)
        request_bytes = request.to_bytes()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(request_bytes)

            response_bytes = s.recv(1024)
            response = HttpResponse.from_bytes(response_bytes)

        return json.dumps(response.body, indent=2)
