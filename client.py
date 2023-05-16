import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("81.169.141.81", 8888))
#client.connect(("localhost", 8888))


while True:

    message = client.recv(1024).decode()
    client.send(input(message).encode())
    message = client.recv(1024).decode()
    client.send(input(message).encode())
    response = client.recv(1024).decode()
    print(response)

    if response == "Login successful!":
        break