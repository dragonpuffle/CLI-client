import socket

# 1. Создаём сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET - IPv4, SOCK_STREAM - TCP

# 2. Подключаемся к серверу (IP и порт)
server_address = ("127.0.0.1", 2000)  # Локальный сервер на порту 12345
client_socket.connect(server_address)

# 3. Отправляем данные
HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'.encode('utf-8')
message = "Привет, сервер!".encode("utf-8")
client_socket.sendall(HDRS + message)

# 4. Получаем ответ
response = client_socket.recv(1024)  # Получаем до 1024 байт
print("Ответ от сервера:", response.decode())

# 5. Закрываем соединение
client_socket.close()
