import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(("81.169.141.81", 8888))
client.connect(("localhost", 7777))

message = client.recv(1024).decode()
client.send(input(message).encode())

while True:
    message = client.recv(1024).decode()
    client.send(input(message).encode())