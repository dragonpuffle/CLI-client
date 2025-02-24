import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 4010))
server_socket.listen(1)

print('Server waits for connection')
client_socket, client_address = server_socket.accept()
print(f'client {client_address} connected')

data = client_socket.recv(1024).decode('utf-8')
print('Received msg:', data)

HDRS = 'HTTP/1.1 200 OK\r\n' \
       'Content-Type: text/html; charset=utf-8\r\n' \
       '\r\n'.encode('utf-8')
content = 'Server received your msg'.encode('utf-8')

client_socket.sendall(HDRS + content)
client_socket.close()
server_socket.close()


# import socket
#
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# server_address = ('127.0.0.1', 4010)
# client_socket.connect(server_address)
#
# message = 'Hello, server!'.encode("utf-8")
# client_socket.sendall(message)
#
# response = client_socket.recv(1024)
# print('Msg from server', response.decode())
#
# client_socket.close()
