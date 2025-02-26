import base64
import json
import pytest
import toml
from client import HttpRequest, HttpResponse, HttpClient


class TestHttpRequest:
    method = 'POST'
    path = '/send_sms'
    headers = {
        'Host': 'localhost',
        'Authorization': 'Basic 1234567890',
        'Content-Type': 'application/json'
    }
    body = {
        'sender': '123',
        'recipient': '456',
        'message': 'hello'
    }
    body_json = json.dumps(body)
    content_length = len(body_json)

    true_request = HttpRequest(method, path, headers, body)
    true_request_bytes = (
        f'POST {path} HTTP/1.1\r\n'
        f'Host: localhost\r\n'
        f'Authorization: Basic 1234567890\r\n'
        f'Content-Type: application/json\r\n'
        f'Content-Length: {content_length}\r\n\r\n'
        f'{body_json}'
    ).encode()

    def test_to_bytes(self):
        request_bytes = self.true_request.to_bytes()

        assert request_bytes == self.true_request_bytes

    def test_from_bytes(self):
        request = HttpRequest.from_bytes(self.true_request_bytes)

        assert request.method == self.method
        assert request.path == self.path
        assert request.headers == self.headers
        assert request.body == self.body

    def test_transform(self):
        assert self.true_request_bytes == HttpRequest.from_bytes(self.true_request_bytes).to_bytes()

        request = HttpRequest.from_bytes(self.true_request.to_bytes())
        assert request.method == self.method
        assert request.path == self.path
        assert request.headers == self.headers
        assert request.body == self.body


class TestHttpResponse:
    status_code = 200
    body = {
        'status': 'success',
        'message_id': '123456'
    }
    body_json = json.dumps(body)
    content_length = len(body_json)
    headers = {
        'Content-Type': 'application/json',
        'Content-Length': str(content_length),
        'Date': 'Wed, 26 Feb 2025 11:11:25 GMT'
    }

    true_response = HttpResponse(status_code, headers, body)
    true_response_bytes = (
        f'HTTP/1.1 {status_code} OK\r\n'
        f'Content-Type: application/json\r\n'
        f'Content-Length: {content_length}\r\n'
        f'Date: Wed, 26 Feb 2025 11:11:25 GMT\r\n\r\n'
        f'{body_json}'
    ).encode()

    def test_to_bytes(self):
        response_bytes = self.true_response.to_bytes()

        assert response_bytes == self.true_response_bytes

    def test_from_bytes(self):
        response = HttpResponse.from_bytes(self.true_response_bytes)

        assert response.status_code == self.status_code
        assert response.headers == self.headers
        assert response.body == self.body

    def test_transform(self):
        assert self.true_response_bytes == HttpResponse.from_bytes(self.true_response_bytes).to_bytes()

        response = HttpResponse.from_bytes(self.true_response.to_bytes())
        assert response.status_code == self.status_code
        assert response.headers == self.headers
        assert response.body == self.body


class TestHttpClient:
    config = toml.load('config.toml')
    server_url = config['server']['url']
    username = config['auth']['username']
    password = config['auth']['password']
    auth_header = base64.b64encode(f'{username}:{password}'.encode()).decode()

    path = '/send_sms'
    request_body = {
        'sender': '123',
        'recipient': '456',
        'message': 'hello'
    }
    headers = {
        'Host': 'localhost',
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/json'
    }

    def test_post(self):
        # if the sever is on
        client = HttpClient(self.server_url)
        response = client.post(self.path, self.request_body, self.headers)
        assert response == '{\n  "status": "success",\n  "message_id": "123456"\n}'


# pytest -s test.py -vv
