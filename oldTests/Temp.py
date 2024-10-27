import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('10.78.1.195', 1253))
s.listen(0)

clientsocket, address = s.accept()
print(f"connection from {address} established")
clientsocket.send(bytes("A", "ascii"))
msg = clientsocket.recv(1)
print(msg.decode("ascii"))

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind(('10.78.1.195', 8080))
# sock.listen(2)
# conn, addr = sock.accept()
# data= conn.recv(1024).decode("ascii")
# print(data)
# data= conn.recv(1024).decode("ascii")
# print(data)
# data= conn.recv(1024).decode("ascii")
# print(data)
