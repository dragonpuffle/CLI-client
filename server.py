import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 2000))
server_socket.listen(1)

print("Сервер ждёт подключения...")
client_socket, client_address = server_socket.accept()
print(f"Клиент подключился: {client_address}")

data = client_socket.recv(1024).decode('utf-8')
print("Получено сообщение:", data)

HDRS = 'HTTP/1.1 200 OK\r\n' \
       'Content-Type: text/html; charset=utf-8\r\n' \
       '\r\n'.encode('utf-8')
content = "Сообщение получено!".encode('utf-8')

client_socket.sendall(HDRS + content)
client_socket.close()
server_socket.close()
