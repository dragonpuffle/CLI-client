import json
import socket
from typing import Dict, Self, Tuple


class HttpRequest:
    def __init__(self, method: str, path: str, headers: Dict[str, str], body: dict = None):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body or {}

    def to_bytes(self) -> bytes:
        body_json = json.dumps(self.body)
        self.headers['Content-Length'] = str(len(body_json))
        headers_str = '\r\n'.join(f'{key}: {val}' for key, val in self.headers.items())

        request = (
            f'{self.method} {self.path} HTTP/1.1\r\n'
            f'{headers_str}\r\n\r\n'
            f'{body_json}'
        )

        return request.encode()

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> Self:
        text = binary_data.decode()
        split_other_body = text.split('\r\n\r\n', 1)

        other = split_other_body[0].split('\r\n')
        method, path, _ = other[0].split(' ', 2)
        headers = {key: val for key, val in (line.split(': ', 1) for line in other[1:])}

        body_json = split_other_body[1] if len(split_other_body) > 1 else {}
        body = json.loads(body_json) if int(headers['Content-Length']) > 0 else {}

        return cls(method, path, headers, body)


class HttpResponse:
    def __init__(self, status_code: int, headers: Dict[str, str], body: dict = None):
        self.status_code = status_code
        self.headers = headers
        self.body = body or {}

    def to_bytes(self) -> bytes:
        body_json = json.dumps(self.body)
        headers_str = '\r\n'.join(f'{key}: {val}' for key, val in self.headers.items())
        response = (
            f'HTTP/1.1 {self.status_code} OK\r\n'
            f'{headers_str}\r\n\r\n'
            f'{body_json}'
        )
        return response.encode()

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> Self:
        text = binary_data.decode()
        split_other_body = text.split('\r\n\r\n', 1)

        other = split_other_body[0].split('\r\n')
        status_line = other[0].split(' ', 2)
        status_code = int(status_line[1])
        headers = {key: val for key, val in (line.split(': ', 1) for line in other[1:])}
        body = split_other_body[1] if len(split_other_body) > 1 else {}
        body = json.loads(body) if int(headers['Content-Length']) > 0 else {}

        return cls(status_code, headers, body)


class HttpClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.host, self.port = self.parse_url(base_url)

    def parse_url(self, url: str) -> Tuple[str, int]:
        parts = url.split(':')
        host = parts[1][2:]
        port = int(parts[2])
        return host, port

    def post(self, path: str, body: dict, headers: Dict[str, str]) -> str:
        request = HttpRequest('POST', path, headers, body)
        request_bytes = request.to_bytes()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.port))
                s.sendall(request_bytes)

                response_bytes = s.recv(1024)
                response = HttpResponse.from_bytes(response_bytes)
            except Exception as e:
                return json.dumps({'error': f'Connection failed - {e}'}, indent=2)

        return json.dumps(response.body, indent=2)
