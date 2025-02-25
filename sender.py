import toml
import base64
from client import HttpClient


def send_msg(sender: str, recipient: str, message: str) -> str:
    config = toml.load('config.toml')
    server_url = config['server']['url']
    username = config['auth']['username']
    password = config['auth']['password']

    auth_header = base64.b64encode(f'{username}:{password}'.encode()).decode()

    request_body = {
        'sender': sender,
        'recipient': recipient,
        'message': message
    }

    headers = {
        'Host': 'localhost',
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/json'
    }

    client = HttpClient(server_url)
    response = client.post('/send_sms', request_body, headers)

    return response
